#!/usr/bin/env python3
"""
RIO v5.1 - لغة مستقلة بنحو خاص كامل (بدون تمرير بايثون خام للجُمل)
================================================================
كل قاعدة نحوية هنا هي قاعدة RIO أصيلة لها ترجمتها الصريحة لبايثون.
لا يوجد "تمرير خام" لأي سطر - كل شيء يُفهم صراحة أو يُرفض بخطأ واضح.
(ملاحظة: هذا ينطبق على الجُمل statements فقط - التعبيرات EXPR داخل
الشروط/الحلقات/جهة يمين "=" تُمرَّر لبايثون مباشرة كما هي.)

    الطباعة:      prn EXPR   /   prt EXPR
    المتغيرات:
        VAR = EXPR                       # تعريف/تحديث عادي
        set VAR = EXPR                   # توافق قديم
        VAR += EXPR / -= / *= / /= / //= / %= / **= / &= / |= / ^= / >>= / <<=
        arr[i] = EXPR / obj.field = EXPR / obj.arr[i] = EXPR   # إسناد بالفهرس أو بالنقطة
        a, b = 1, 2   /   a, b = b, a   /   a[0], a[1] = a[1], a[0]   # تفكيك
    الشروط:       if EXPR: / elif EXPR: / else:
    الحلقات:
        rep i in A..B:        # حلقة عداد رقمي
        rep item in EXPR:     # حلقة على أي مجموعة (قائمة، نص، إلخ)
        while EXPR:
        rep N (EXPR)          # الصيغة القديمة: تكرار طباعة، سطر واحد
        break / continue
    الدوال:
        fanc name(args) = EXPR      # دالة بسطر واحد
        fanc name(args):            # دالة بجسم متعدد الأسطر
        return EXPR
        yield EXPR / yield from EXPR   # دوال مولّدة (generators)
        global VAR, ... / nonlocal VAR, ...
    الكلاسات:
        cls Name:
        cls Name(Base1, Base2, ...):    # وراثة
            new(args):               # المُنشئ (constructor)
                me.field = value      # "me" تعادل self
            fanc method(args):
                ...
        Name(args)                    # لإنشاء كائن جديد
        obj.field / obj.method(args)  # وصول عادي
    معالجة الأخطاء:
        try:
            ...
        catch ERR:                       # أو catch:  بدون اسم
        catch (Type1, Type2) ERR:        # أنواع أخطاء متعددة، مع متغير أو بدونه
        catch (Type1, Type2):
            ...
        finally:
            ...
        fail EXPR        # رمي خطأ (زي raise)
        assert EXPR [, MESSAGE]
    سياقات:       with EXPR as VAR:   / with EXPR:
    دمج النصوص:  "نص فيه {متغير}" - بدون حاجة لبادئة f يدوياً
    أخرى:        input / import / from import / draw / use "file.rio" (كما بالإصدار السابق)
"""

import re
import sys
import os
import difflib

VERSION = "RIO v5.1"
IDENT_RE = r"[A-Za-z_][A-Za-z0-9_]*"

KNOWN_KEYWORDS = [
    "prn", "prt", "set", "rep", "fanc", "return", "cls", "new", "try",
    "catch", "finally", "fail", "if", "elif", "else", "while", "input",
    "import", "from", "draw", "use", "break", "continue", "yield",
    "global", "nonlocal", "assert", "with",
]


class RioError(Exception):
    pass


def strip_comment(line):
    in_str = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_str = not in_str
        if ch == "#" and not in_str:
            return line[:i]
    return line


def get_indent(line):
    expanded = line.replace("\t", "    ")
    return len(expanded) - len(expanded.lstrip(" "))


def interpolate(text):
    """يحول أي سلسلة نصية "...{expr}..." لبايثون f-string تلقائياً، بدون
    الحاجة إن المستخدم يكتب f يدوياً - جزء من نحو RIO الأصيل."""
    def repl(m):
        start = m.start()
        already_f = start > 0 and text[start - 1] in ("f", "F")
        content = m.group(1)
        if already_f or "{" not in content:
            return m.group(0)
        return f'f"{content}"'
    return re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', repl, text)


def suggest_keyword(word):
    """يقترح أقرب كلمة مفتاحية RIO معروفة لكلمة كتبها المستخدم بالغلط."""
    matches = difflib.get_close_matches(word.lower(), KNOWN_KEYWORDS, n=1, cutoff=0.6)
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# المترجم الرئيسي - يتتبع مكدس الكتل المفتوحة حسب المسافة البادئة
# يدعم use "file.rio" للاستيراد بين ملفات RIO (تضمين نصي recursive)
# ---------------------------------------------------------------------------

def transpile_lines(source: str, base_dir: str, visited: set) -> tuple:
    """يرجع (قائمة أسطر بايثون مُولّدة, هل تحتاج turtle) لملف RIO واحد."""
    lines = source.split("\n")
    out = []
    needs_turtle = False
    block_stack = []  # كل عنصر: (indent_len, kind)

    for raw_idx, raw in enumerate(lines):
        line_no = raw_idx + 1
        line = strip_comment(raw.replace("\t", "    ")).rstrip()
        if not line.strip():
            out.append("")
            continue

        indent_len = get_indent(line)
        stripped = line.strip()
        low = stripped.lower()

        # إغلاق أي كتل انتهت (رجعت المسافة البادئة لمستواها أو أقل)
        while block_stack and indent_len <= block_stack[-1][0]:
            block_stack.pop()

        inside_cls = any(k == "cls" for _, k in block_stack)
        indent = " " * indent_len

        def put(code, push=None):
            if inside_cls:
                code = re.sub(rf"\bme\b", "self", code)
            out.append(indent + interpolate(code))
            if push:
                block_stack.append((indent_len, push))

        # ---- use "file.rio"  : تضمين ملف RIO آخر ----
        m = re.match(r'use\s+"([^"]+)"\s*$', stripped, re.IGNORECASE)
        if m:
            rel_path = m.group(1)
            full_path = os.path.normpath(os.path.join(base_dir, rel_path))
            if full_path in visited:
                continue  # تم تضمينه قبل كذا - تفادي التكرار/الحلقات الدائرية
            if not os.path.isfile(full_path):
                raise RioError(f"سطر {line_no}: ملف مستخدم بـ use غير موجود: {rel_path!r}")
            visited.add(full_path)
            with open(full_path, encoding="utf-8") as f:
                included_source = f.read()
            included_lines, included_needs_turtle = transpile_lines(
                included_source, os.path.dirname(full_path), visited
            )
            out.append(f"# ----- بداية {rel_path} (عبر use) -----")
            out.extend(included_lines)
            out.append(f"# ----- نهاية {rel_path} -----")
            needs_turtle = needs_turtle or included_needs_turtle
            continue

        # ---- cls Name: / cls Name(Base1, Base2): [وراثة] ----
        m = re.match(rf"cls\s+({IDENT_RE})\s*(?:\(([^)]*)\))?\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            name, bases = m.groups()
            put(f"class {name}({bases.strip()}):" if bases and bases.strip() else f"class {name}:", push="cls")
            continue

        # ---- new(args):  [مُنشئ الكلاس، لازم يكون مباشرة داخل cls] ----
        m = re.match(rf"new\s*\((.*)\)\s*:\s*$", stripped, re.IGNORECASE)
        if m and block_stack and block_stack[-1][1] == "cls":
            args = m.group(1).strip()
            sig = "self, " + args if args else "self"
            put(f"def __init__({sig}):", push="fanc")
            continue

        # ---- fanc method(args):  داخل كلاس -> تُضاف self تلقائياً ----
        m = re.match(rf"fanc\s+({IDENT_RE})\s*\((.*)\)\s*:\s*$", stripped, re.IGNORECASE)
        if m and block_stack and block_stack[-1][1] == "cls":
            name, args = m.group(1), m.group(2).strip()
            sig = "self, " + args if args else "self"
            put(f"def {name}({sig}):", push="fanc")
            continue

        # ---- fanc name(args) = expr  [سطر واحد، مستوى عام] ----
        m = re.match(rf"fanc\s+({IDENT_RE})\s*\((.*)\)\s*=\s*(.+)$", stripped, re.IGNORECASE)
        if m:
            name, args, expr = m.groups()
            put(f"def {name}({args}): return {expr}")
            continue

        # ---- fanc name(args):  [عام، خارج أي كلاس] ----
        m = re.match(rf"fanc\s+({IDENT_RE})\s*\((.*)\)\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            name, args = m.groups()
            put(f"def {name}({args}):", push="fanc")
            continue

        # ---- return ----
        if low == "return":
            put("return")
            continue
        if low.startswith("return "):
            put(f"return {stripped[7:]}")
            continue

        # ---- yield / yield from EXPR ----
        if low == "yield":
            put("yield")
            continue
        if low.startswith("yield "):
            put(f"yield {stripped[6:]}")
            continue

        # ---- break / continue ----
        if low == "break":
            put("break")
            continue
        if low == "continue":
            put("continue")
            continue

        # ---- global / nonlocal ----
        m = re.match(r"(global|nonlocal)\s+(.+)$", stripped, re.IGNORECASE)
        if m:
            put(f"{m.group(1).lower()} {m.group(2)}")
            continue

        # ---- assert EXPR [, MESSAGE] ----
        if low.startswith("assert "):
            put(f"assert {stripped[7:]}")
            continue

        # ---- with EXPR [as VAR][, EXPR2 as VAR2...]: ----
        m = re.match(r"with\s+(.+):\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"with {m.group(1)}:", push="with")
            continue

        # ---- try / catch / finally / fail ----
        if low == "try:":
            put("try:", push="try")
            continue
        m = re.match(rf"catch\s+({IDENT_RE})\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"except Exception as {m.group(1)}:", push="catch")
            continue
        # ---- catch (Type1, Type2) VAR:  /  catch (Type1, Type2):  [أنواع أخطاء متعددة] ----
        m = re.match(rf"catch\s*\(([^)]+)\)\s*({IDENT_RE})\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            types, var = m.groups()
            put(f"except ({types.strip()}) as {var}:", push="catch")
            continue
        m = re.match(rf"catch\s*\(([^)]+)\)\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"except ({m.group(1).strip()}):", push="catch")
            continue
        if low == "catch:":
            put("except:", push="catch")
            continue
        if low == "finally:":
            put("finally:", push="finally")
            continue
        if low == "fail":
            put("raise")
            continue
        if low.startswith("fail "):
            fail_expr = stripped[5:].strip()
            put(f"raise Exception({fail_expr})")
            continue

        # ---- input ----
        m = re.match(rf"input\s+({IDENT_RE})\s*(.*)$", stripped, re.IGNORECASE)
        if m:
            var, rest = m.group(1), m.group(2).strip()
            put(f"{var} = input({rest})" if rest else f"{var} = input()")
            continue

        # ---- from MODULE import NAME [as ALIAS] ----
        m = re.match(rf"from\s+([A-Za-z_][\w.]*)\s+import\s+({IDENT_RE})\s*(as\s+({IDENT_RE}))?\s*$",
                     stripped, re.IGNORECASE)
        if m:
            module, name, _, alias = m.groups()
            put(f"from {module} import {name} as {alias}" if alias else f"from {module} import {name}")
            continue

        # ---- import MODULE [as ALIAS] ----
        m = re.match(rf"import\s+([A-Za-z_][\w.]*)\s*(as\s+({IDENT_RE}))?\s*$", stripped, re.IGNORECASE)
        if m:
            module, _, alias = m.groups()
            put(f"import {module} as {alias}" if alias else f"import {module}")
            continue

        # ---- rep i in A..B:  [حلقة عداد رقمي] ----
        m = re.match(rf"rep\s+({IDENT_RE})\s+in\s+(.+?)\.\.(.+?):\s*$", stripped, re.IGNORECASE)
        if m:
            var, a, b = m.groups()
            put(f"for {var} in range({a}, ({b}) + 1):", push="rep")
            continue

        # ---- rep item in EXPR:  [حلقة على أي مجموعة] ----
        m = re.match(rf"rep\s+({IDENT_RE})\s+in\s+(.+?):\s*$", stripped, re.IGNORECASE)
        if m:
            var, iterable = m.groups()
            put(f"for {var} in {iterable}:", push="rep")
            continue

        # ---- rep N (EXPR)  [صيغة قديمة: تكرار طباعة، سطر واحد] ----
        m = re.match(r"rep\s+(\S+)\s*\((.*)\)\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"for _ in range({m.group(1)}): print({m.group(2)})")
            continue

        # ---- while EXPR: ----
        m = re.match(r"while\s+(.+?):\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"while {m.group(1)}:", push="while")
            continue

        # ---- if / elif / else ----
        m = re.match(r"if\s+(.+?):\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"if {m.group(1)}:", push="if")
            continue
        m = re.match(r"elif\s+(.+?):\s*$", stripped, re.IGNORECASE)
        if m:
            put(f"elif {m.group(1)}:", push="if")
            continue
        if low == "else:":
            put("else:", push="if")
            continue

        # ---- draw ----
        m = re.match(r"draw\s+circle\s+(\S+)\s*$", stripped, re.IGNORECASE)
        if m:
            needs_turtle = True
            put(f"_rio_turtle.circle({m.group(1)})")
            continue
        m = re.match(r"draw\s+line\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$", stripped, re.IGNORECASE)
        if m:
            needs_turtle = True
            x1, y1, x2, y2 = m.groups()
            put(f"_rio_turtle.penup(); _rio_turtle.goto({x1}, {y1}); "
                f"_rio_turtle.pendown(); _rio_turtle.goto({x2}, {y2})")
            continue

        # ---- prn / prt ----
        if low == "prn" or low.startswith("prn "):
            expr = stripped[3:].strip() if low != "prn" else '""'
            put(f"print({expr})")
            continue
        if low.startswith("prt "):
            put(f'print({stripped[3:].strip()}, end="")')
            continue

        # ---- هدف إسناد عام: VAR أو VAR.attr أو VAR[index] أو سلسلة منهم ----
        TARGET_RE = rf"{IDENT_RE}(?:\.{IDENT_RE}|\[[^\[\]]*\])*"
        AUG_OPS = r"\*\*|//|>>|<<|\+|-|\*|/|%|&|\||\^"

        # ---- عوامل الإسناد المركّب: VAR += EXPR  (وأيضاً -= *= /= //= %= **= &= |= ^= >>= <<=) ----
        m = re.match(rf"^({TARGET_RE})\s*({AUG_OPS})=\s*(.+)$", stripped)
        if m:
            target, op, expr = m.groups()
            put(f"{target} {op}= {expr}")
            continue

        # ---- set VAR = EXPR (توافق قديم، اختيارية) ----
        m = re.match(rf"set\s+({IDENT_RE})\s*=\s*(.+)$", stripped, re.IGNORECASE)
        if m:
            put(f"{m.group(1)} = {m.group(2)}")
            continue

        # ---- تفكيك: a, b, c = EXPR1, EXPR2, ...  (يدعم أهداف مفهرسة/منقّطة زي a[0], a[1] = ...) ----
        m = re.match(rf"^({TARGET_RE}(?:\s*,\s*{TARGET_RE})+)\s*=\s*(.+)$", stripped)
        if m:
            targets, expr = m.groups()
            put(f"{targets} = {expr}")
            continue

        # ---- VAR = EXPR (تحديث/تعريف عادي) ----
        m = re.match(rf"({IDENT_RE})\s*=\s*(.+)$", stripped)
        if m and m.group(1).lower() not in ("if", "elif", "while", "fanc", "rep", "set", "cls", "new", "catch"):
            put(f"{m.group(1)} = {m.group(2)}")
            continue

        # ---- إسناد بالفهرس أو بسلسلة .attr/[index]: arr[0] = EXPR / obj.arr[i] = EXPR ----
        m = re.match(rf"^({TARGET_RE})\s*=\s*(.+)$", stripped)
        if m and ("[" in m.group(1) or "." in m.group(1)):
            put(f"{m.group(1)} = {m.group(2)}")
            continue

        # ---- جملة استدعاء/وصول مستقلة: name(...) أو obj.attr(...) ----
        if re.match(rf"^{IDENT_RE}(\.{IDENT_RE})*\s*\(.*\)\s*$", stripped) or \
           re.match(rf"^{IDENT_RE}(\.{IDENT_RE})+\s*=\s*.+$", stripped):
            put(stripped)
            continue

        raise RioError(f"سطر غير مفهوم بنحو RIO (سطر {line_no}): {stripped!r}{_did_you_mean(stripped)}")

    return out, needs_turtle


def _did_you_mean(stripped_line: str) -> str:
    first_word = stripped_line.split(" ", 1)[0].strip(":()=")
    suggestion = suggest_keyword(first_word)
    if suggestion and suggestion.lower() != first_word.lower():
        return f"\n  💡 هل تقصد '{suggestion}'؟"
    return ""


def transpile(source: str, base_dir: str = ".") -> str:
    out, needs_turtle = transpile_lines(source, base_dir, visited=set())
    header = []
    if needs_turtle:
        header = ["import turtle as _t", "_rio_turtle = _t.Turtle()", ""]
    return "\n".join(header) + "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# كاشف الأخطاء البسيط والمحافظ
# ---------------------------------------------------------------------------
# يتحقق فقط مما هو متأكد منه 100٪ (عدد معاملات الدوال fanc وكلاسات cls)
# عشان ما يعطي نتائج كاذبة. يقرأ نفس الملفات المُضمَّنة عبر use أيضاً.

def _collect_source(source, base_dir, visited):
    """يجمع كل أسطر الملف + كل الملفات المُضمَّنة عبر use بملف واحد للفحص."""
    all_lines = []
    for raw in source.split("\n"):
        stripped = strip_comment(raw).strip()
        m = re.match(r'use\s+"([^"]+)"\s*$', stripped, re.IGNORECASE)
        if m:
            full_path = os.path.normpath(os.path.join(base_dir, m.group(1)))
            if full_path in visited or not os.path.isfile(full_path):
                continue
            visited.add(full_path)
            with open(full_path, encoding="utf-8") as f:
                included = f.read()
            all_lines.extend(_collect_source(included, os.path.dirname(full_path), visited))
        else:
            all_lines.append(raw)
    return all_lines


def analyze(source: str, base_dir: str = "."):
    lines = _collect_source(source, base_dir, set())
    functions = {}   # اسم الدالة -> عدد المعاملات (fanc عادية، خارج أي كلاس)
    classes = {}      # اسم الكلاس -> عدد معاملات new (بدون me)
    errors = []

    cls_stack = []  # لتتبع هل نحن داخل جسم كلاس أثناء رؤية fanc
    for raw in lines:
        stripped = strip_comment(raw).strip()
        if not stripped:
            continue
        indent = get_indent(raw.replace("\t", "    "))
        while cls_stack and indent <= cls_stack[-1]:
            cls_stack.pop()

        m = re.match(rf"cls\s+({IDENT_RE})\s*(?:\([^)]*\))?\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            cls_stack.append(indent)
            continue

        if not cls_stack:  # fanc عادية خارج أي كلاس فقط
            m = re.match(rf"fanc\s+({IDENT_RE})\s*\((.*)\)\s*(=.*|:)\s*$", stripped, re.IGNORECASE)
            if m:
                params = [p.strip() for p in m.group(2).split(",") if p.strip()]
                functions[m.group(1)] = len(params)
                continue

    # مرور ثاني: ربط new() بالكلاس الصحيح (مكدس مستقل يحمل اسم الكلاس مع كل مستوى)
    cls_stack2 = []  # (indent, class_name)
    for raw in lines:
        stripped = strip_comment(raw).strip()
        if not stripped:
            continue
        indent = get_indent(raw.replace("\t", "    "))
        while cls_stack2 and indent <= cls_stack2[-1][0]:
            cls_stack2.pop()
        m = re.match(rf"cls\s+({IDENT_RE})\s*(?:\([^)]*\))?\s*:\s*$", stripped, re.IGNORECASE)
        if m:
            cls_stack2.append((indent, m.group(1)))
            continue
        m = re.match(r"new\s*\((.*)\)\s*:\s*$", stripped, re.IGNORECASE)
        if m and cls_stack2:
            params = [p.strip() for p in m.group(1).split(",") if p.strip()]
            classes[cls_stack2[-1][1]] = len(params)

    # فحص الاستدعاءات
    for idx, raw in enumerate(lines, start=1):
        stripped = strip_comment(raw).strip()
        if not stripped:
            continue
        if re.match(rf"cls\s+{IDENT_RE}\s*(?:\([^)]*\))?\s*:\s*$", stripped, re.IGNORECASE):
            continue  # سطر تعريف كلاس (زي cls Dog(Animal):) مو استدعاء - تجاهله
        for call_m in re.finditer(rf"({IDENT_RE})\s*\(([^()]*)\)", stripped):
            name, args_text = call_m.group(1), call_m.group(2)
            if stripped[:call_m.start()].rstrip().endswith("."):
                continue  # obj.method(...) - مو دالة/كلاس RIO مباشر
            actual = len([a for a in args_text.split(",") if a.strip()])
            if name in functions:
                expected = functions[name]
                if actual != expected:
                    errors.append(f"سطر {idx}: الدالة '{name}' تتوقع {expected} معامل لكن استُدعيت بـ {actual}")
            elif name in classes:
                expected = classes[name]
                if actual != expected:
                    errors.append(f"سطر {idx}: الكلاس '{name}' يتوقع {expected} معامل بـ new لكن استُدعي بـ {actual}")

    return errors


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{VERSION} - الاستخدام: python rio.py file.rio [--run]  (امتداد .f مقبول أيضاً)")
        sys.exit(1)

    file_path = sys.argv[1]
    if not (file_path.endswith(".rio") or file_path.endswith(".f")):
        print("تنبيه: الامتداد المعتاد هو .rio أو .f — بمتابعة التشغيل على أي حال.")

    with open(file_path, encoding="utf-8") as f:
        source = f.read()

    base_dir = os.path.dirname(os.path.abspath(file_path))

    errors = analyze(source, base_dir)
    if errors:
        for e in errors:
            print("✗ ", e)
        print("\nتم إيقاف الترجمة بسبب الأخطاء أعلاه.")
        sys.exit(1)

    try:
        py_code = transpile(source, base_dir=base_dir)
    except RioError as e:
        print(f"خطأ في لغة {VERSION}: {e}")
        sys.exit(1)

    print(f"----- الكود المُولَّد ({VERSION}) -----")
    print(py_code)
    if "--run" in sys.argv:
        print("----- الناتج -----")
        exec(py_code, {})

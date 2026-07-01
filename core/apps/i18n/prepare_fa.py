import os
import shutil
import polib

ROOT = os.path.dirname(os.path.abspath(__file__))


def clear_po(po_path):
    po = polib.pofile(po_path)

    for entry in po:
        # Clear normal translation
        entry.msgstr = ""

        # Clear plural translations
        if entry.msgstr_plural:
            for key in list(entry.msgstr_plural.keys()):
                entry.msgstr_plural[key] = ""

        # Mark as untranslated
        if "fuzzy" in entry.flags:
            entry.flags.remove("fuzzy")

        entry.previous_msgid = None

    po.save()


def prepare_locale(directory):
    zh_locale = os.path.join(directory, "zh", "LC_MESSAGES")

    if not os.path.isdir(zh_locale):
        return

    fa_locale = os.path.join(directory, "fa", "LC_MESSAGES")
    os.makedirs(fa_locale, exist_ok=True)

    for filename in os.listdir(zh_locale):
        if not filename.endswith(".po"):
            continue

        src = os.path.join(zh_locale, filename)
        dst = os.path.join(fa_locale, filename)

        shutil.copy2(src, dst)
        clear_po(dst)

        print(f"Prepared {dst}")


def copy_json(directory):
    zh_json = os.path.join(directory, "zh.json")

    if not os.path.exists(zh_json):
        return

    fa_json = os.path.join(directory, "fa.json")

    if not os.path.exists(fa_json):
        shutil.copy2(zh_json, fa_json)
        print(f"Copied {fa_json}")


def main():
    for name in os.listdir(ROOT):
        if name.startswith("_"):
            continue

        path = os.path.join(ROOT, name)

        if not os.path.isdir(path):
            continue

        prepare_locale(path)
        copy_json(path)

    print("\nDone!")
    print("All Persian .po files are prepared.")
    print("All Persian JSON files have been copied.")


if __name__ == "__main__":
    main()
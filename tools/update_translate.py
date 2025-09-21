import pathlib
import re
import subprocess

here: pathlib.Path = pathlib.Path(__file__).parent


def main():
    labelme_path: pathlib.Path = here / ".." / "labelme"
    labelme_files: list[pathlib.Path] = list(labelme_path.rglob("*.py"))

    LANGUAGES: list[str] = ["zh_CN"]
    labelme_translate_path: pathlib.Path = labelme_path / "translate"
    for lang in LANGUAGES:
        ts_path: pathlib.Path = labelme_translate_path / f"{lang}.ts"
        subprocess.check_call(
            [
                "pylupdate5",
                *labelme_files,
                "-ts",
                str(ts_path),
            ]
        )
        assert ts_path.exists()

        # Zero out line numbers to reduce unnecessary diffs in .ts file
        ts_content: str = ts_path.read_text()
        new_ts_content: str = re.sub(r'line="\d+"', 'line="0"', ts_content)
        assert ts_content.strip() != new_ts_content.strip()
        ts_path.write_text(new_ts_content)

        qm_path: pathlib.Path = labelme_translate_path / f"{lang}.qm"
        subprocess.check_call(["lrelease", ts_path, "-qm", qm_path])
        assert qm_path.exists()


if __name__ == "__main__":
    main()

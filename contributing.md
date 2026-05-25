# Contribution Guidelines

Thank you for taking the time to contribute to Awesome Bio Agent Skills!

Please note that this project is released with a [Contributor Code of Conduct](code-of-conduct.md). By participating in this project you agree to abide by its terms.

## Adding a Skill

To add a new skill to this list, open a pull request with the following:

### Checklist

- [ ] The skill is a self-contained folder with a `SKILL.md` file.
- [ ] The skill covers a biomedical or bioinformatics topic not already represented.
- [ ] The skill has been tested and produces scientifically meaningful outputs.
- [ ] The source repository is publicly accessible and actively maintained.
- [ ] Your entry follows the format below exactly.

### Entry Format

Add your entry to the appropriate category table in `README.md`:

```markdown
| [skill-name](skills/<source>/<skill-name>/) | source | One-sentence description starting uppercase and ending with a period. |
```

Rules:
- The skill name links to its folder path in this repository.
- The description starts with an uppercase character and ends with a period.
- The description is objective — no marketing language, no superlatives.
- The description is concise (one sentence, under 120 characters preferred).
- Add the entry at the bottom of the appropriate category table.

### Updating the Index

After adding the skill folder, update `bioskill_index_v2.csv` with a new row:

```
skill_name,folder_name,source_repo,category,description,file_count,archive_path
```

## Removing a Skill

Open a pull request with a clear explanation of why the skill should be removed (e.g., the source repository has been archived, the skill is broken, or it duplicates an existing entry).

## Updating an Existing Entry

If a skill description is inaccurate or a link is broken, open a pull request with the correction and a brief explanation.

## Pull Request Guidelines

- One pull request per skill addition, removal, or correction.
- The pull request title should be in the format: `Add <skill-name>` or `Fix <skill-name>`.
- Do not restructure categories or reorder existing entries in the same pull request as an addition.
- Check your spelling and grammar before submitting.

## Updating Your Pull Request

If a maintainer requests changes, amend your commit and force-push to your branch. Do not open a new pull request.

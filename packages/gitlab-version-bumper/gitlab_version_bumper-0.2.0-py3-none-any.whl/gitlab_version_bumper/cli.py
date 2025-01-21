"""
This python function is intended to be used in the CI chain
to bump the prerelase info for production pipeline
Return to stdout: The new version string or a error message
"""

import os
import subprocess
import semver
import click


@click.command()
@click.option(
    "--versionfile",
    "-f",
    type=click.File("r"),
    help="Version information file for upcoming version",
)
@click.option(
    "--integration_branch",
    "-m",
    default="main",
    show_default=True,
    help="The integration branch name.",
)
@click.option(
    "--pre_release_token_integration",
    "-i",
    default="beta",
    show_default=True,
    help="The pre-release token which will be added when merging into integration branch.",
)
@click.option(
    "--pre_release_token_branch",
    "-b",
    default="alpha",
    show_default=True,
    help="The pre-release token which will be added when working on a feature branch.",
)
def main(
    versionfile,
    integration_branch,
    pre_release_token_integration,
    pre_release_token_branch,
):
    """This python function is intended to be used in the CI chain
    to bump the prerelase info for production pipeline
    Return to stdout: The new version string or a error message"""

    commit_tag = os.environ.get("CI_COMMIT_TAG")
    is_protected = os.environ.get("CI_COMMIT_REF_PROTECTED") == "true"
    build_id = os.environ.get("CI_PIPELINE_IID")
    prerelease_id = (
        pre_release_token_integration
        if os.environ.get("CI_COMMIT_BRANCH") == integration_branch
        else pre_release_token_branch
    )

    if commit_tag and is_protected:
        print(semver.Version.parse(str(commit_tag)))
        return

    if versionfile is None:
        published_tag = semver.Version.parse(
            subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"])
            .decode("ascii")
            .strip()
        )
        current_version = published_tag.bump_patch().replace(
            prerelease=prerelease_id, build=build_id
        )
        print(semver.Version.parse(str(current_version)))
        return

    # Read the version information from file
    published_tag = semver.Version.parse(versionfile.read())
    current_version = published_tag.replace(prerelease=f"{prerelease_id}.{build_id}")

    # double check, that we end up with a valid version
    print(semver.Version.parse(str(current_version)))


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter

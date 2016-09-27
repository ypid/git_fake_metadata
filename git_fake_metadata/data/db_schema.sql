-- Schema for git_fake_metadata

create table version (
    version text
);

create table last_action (
    vcs_repo_path text,
    timestamp     timestamp
);

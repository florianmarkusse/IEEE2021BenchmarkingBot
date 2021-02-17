# PR (Pull Request) Data salesforce/lwc

This directory contains the PR data for the salesforce/lwc project. The files have the following contents:

- **botPRData.json**: This file contains all the PR's from 2019-07-29 (yyyy-mm-dd) until currentDate where the benchmark bot contributed in.
- **allPRData.json**: This file contains all the PR's from 2019-07-29 (yyyy-mm-dd) until currentDate.

# PR features

The data collected from each PR is the following (note that the data may have changed at the time of viewing):
- **cursor**: This is a unique ID and is only used for pagination to retrieve all the data.
- **title**: This is the current title of the PR.
- **createdAt** (): The date the PR was created.
- **merged**: Whether or not the PR was merged.
- **mergedAt**: The date of when the PR was merged. (_null_ if not applicable)
- **closed**: Whether or not the PR was closed.
- **closedAt**: The date of when the PR was closed. (_null_ if not applicable)
- **participants/totalCount**: The number of participants in this PR.
- **reviews/totalCount**: The number of reviews in this PR.
- **comments/totalCount**: The number of comments in this PR.
- **commits/totalCount**: The number of commits in this PR.
- **additions**: The number of lines this PR adds
- **deletions**: The number of lines this PR deletes. 


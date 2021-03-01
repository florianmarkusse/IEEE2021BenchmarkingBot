from utility import file_management

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

for project in projects:
  # Get bot PR data
  # Write to file
  print(project.get("owner"))
  # Get all PR data
  # Write to file

  # Create README.md in folder


from github import Github
import os


def add_skill_to_github(skill):
    github_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    g = Github(github_token)
    repo_name = "insshubh/overleafData"  # Replace with your actual repo name

    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        raise ValueError(f"Could not access repo {repo_name}: {e}")

    file_path = "my_file"  # Replace with your actual file path
    try:
        contents = repo.get_contents(file_path)
        content = contents.decoded_content.decode()

        # Find the "Technical Skills" section
        skills_section_start = content.find(r'\section{Technical Skills}')
        if skills_section_start == -1:
            raise ValueError("Technical Skills section not found")

        # Find the end of the "Technical Skills" section
        skills_list_start = content.find(r'\begin{itemize}', skills_section_start)
        if skills_list_start == -1:
            raise ValueError("Start of skills list not found")

        skills_list_end = content.find(r'\end{itemize}', skills_list_start)
        if skills_list_end == -1:
            raise ValueError("End of skills list not found")

        # Insert the new skill before the end of the itemize environment
        new_content = content[:skills_list_end] + f'  \\item {skill}\n' + content[skills_list_end:]

        repo.update_file(contents.path, f"Add skill {skill}", new_content, contents.sha)
    except Exception as e:
        raise ValueError(f"Could not update file {file_path}: {e}")


def add_certificate_to_github(certificate):
    github_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    g = Github(github_token)
    repo_name = "insshubh/overleafData"  # Replace with your actual repo name

    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        raise ValueError(f"Could not access repo {repo_name}: {e}")

    file_path = "my_file"  # Replace with your actual file path
    try:
        contents = repo.get_contents(file_path)
        content = contents.decoded_content.decode()

        # Find the "Certification" section
        cert_section_start = content.find(r'\section{Certification}')
        if cert_section_start == -1:
            raise ValueError("Certification section not found")

        # Find the end of the "Certification" section
        cert_list_start = content.find(r'\begin{itemize}', cert_section_start)
        if cert_list_start == -1:
            raise ValueError("Start of certification list not found")

        cert_list_end = content.find(r'\end{itemize}', cert_list_start)
        if cert_list_end == -1:
            raise ValueError("End of certification list not found")

        # Insert the new certificate before the end of the itemize environment
        new_content = content[:cert_list_end] + f'  \\item {certificate}\n' + content[cert_list_end:]

        repo.update_file(contents.path, f"Add certificate {certificate}", new_content, contents.sha)
    except Exception as e:
        raise ValueError(f"Could not update file {file_path}: {e}")

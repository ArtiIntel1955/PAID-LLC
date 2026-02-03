import os
import subprocess
import sys
from pathlib import Path

def setup_github_repository():
    """
    Script to set up a GitHub repository for PAID LLC website
    """
    print("Setting up GitHub repository for PAID LLC website...")
    
    # GitHub repository details
    github_username = "ArtiIntel1955"
    repo_name = f"{github_username}.github.io"
    
    print(f"Repository name will be: {repo_name}")
    print(f"This will create a GitHub Pages site at: https://{github_username}.github.io/")
    
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✓ Git is installed")
    except subprocess.CalledProcessError:
        print("✗ Git is not installed. Please install Git first.")
        return False
    
    # Check if we have GitHub credentials
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("\n⚠️  GitHub Personal Access Token not found!")
        print("Please set the GITHUB_TOKEN environment variable with your GitHub PAT.")
        print("\nTo create a GitHub PAT:")
        print("1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)")
        print("2. Click 'Generate new token'")
        print("3. Select 'public_repo' scope (or 'repo' for private repos)")
        print("4. Copy the generated token")
        print("5. Set it as an environment variable: export GITHUB_TOKEN='your_token_here'")
        print("6. Or save it to a file and reference it in your OpenClaw config")
        return False
    
    # Create a temporary directory for the repository
    temp_dir = Path("temp_github_repo")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Change to the temporary directory
        os.chdir(temp_dir)
        
        # Initialize git repository
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", github_username], check=True)
        subprocess.run(["git", "config", "user.email", f"{github_username}@users.noreply.github.com"], check=True)
        
        print(f"✓ Initialized git repository in {temp_dir}")
        
        # Copy website files to the repository
        import shutil
        
        # Copy the premium website as index.html
        if Path("../index_premium.html").exists():
            shutil.copy("../index_premium.html", "index.html")
            print("✓ Copied premium website as index.html")
        elif Path("../index.html").exists():
            shutil.copy("../index.html", "index.html")
            print("✓ Copied basic website as index.html")
        else:
            print("✗ No website files found to copy")
            return False
        
        # Create additional files for GitHub Pages
        # robots.txt
        with open("robots.txt", "w") as f:
            f.write("User-agent: *\nAllow: /\n")
        
        # .nojekyll to enable files and folders starting with underscores
        with open(".nojekyll", "w") as f:
            pass
        
        print("✓ Created additional GitHub Pages files")
        
        # Add files to git
        subprocess.run(["git", "add", "."], check=True)
        print("✓ Added files to git staging")
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", "Initial commit: PAID LLC website"], check=True)
        print("✓ Committed changes")
        
        # Add remote origin
        repo_url = f"https://{github_username}:{token}@github.com/{github_username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        print("✓ Added remote origin")
        
        # Push to GitHub
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        result = subprocess.run(["git", "push", "-u", "origin", "main"], check=True, capture_output=True, text=True)
        
        print("✓ Pushed changes to GitHub")
        print(f"\n🎉 Success! Your website is now deployed at: https://{github_username}.github.io/")
        print(f"You can visit your repository at: https://github.com/{github_username}/{repo_name}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during git operations: {e}")
        print("Details:", e.stderr)
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    finally:
        # Clean up: remove the temporary directory
        os.chdir("..")
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"✓ Cleaned up temporary directory")

if __name__ == "__main__":
    success = setup_github_repository()
    if success:
        print("\n✅ Repository setup completed successfully!")
    else:
        print("\n❌ Repository setup failed. Please check the errors above.")
        print("\nMake sure you have:")
        print("1. A valid GitHub Personal Access Token with repo permissions")
        print("2. Git installed on your system")
        print("3. Internet connectivity")
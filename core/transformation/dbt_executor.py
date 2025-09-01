import os
import subprocess
import webbrowser

def run_dbt_command(command: str, dbt_dir: str, profiles_dir: str) -> int:
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = profiles_dir
    process = subprocess.run(command, shell=True, cwd=dbt_dir, env=env)
    return process.returncode


def run_dbt_seed(dbt_dir: str, profiles_dir: str) -> int:
    return run_dbt_command("dbt seed", dbt_dir, profiles_dir)


def run_dbt_run(dbt_dir: str, profiles_dir: str) -> int:
    return run_dbt_command("dbt run", dbt_dir, profiles_dir)


def run_dbt_test(dbt_dir: str, profiles_dir: str) -> int:
    return run_dbt_command("dbt test", dbt_dir, profiles_dir)


def open_dbt_docs(dbt_dir: str, profiles_dir: str) -> None:
    # Start dbt docs serve in background
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = profiles_dir
    # Generate docs first
    # subprocess.run("dbt docs generate", shell=True, cwd=dbt_dir, env=env)
    # Start dbt docs serve in background
    # kill anything on port 8082
    try:
        # Find process using port 8082 and kill it (works on Unix)
        subprocess.run("lsof -ti:8082 | xargs kill -9", shell=True, check=False)
    except Exception as e:
        print(f"Warning: Could not kill process on port 8082: {e}")
    process = subprocess.Popen("dbt docs serve --port 8082", shell=True, cwd=dbt_dir, env=env)
    # Open docs in browser (port 8082)
    webbrowser.open("http://localhost:8082")


def execute_all(database_name):
    import shutil
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dbt_dir = os.path.join(base_dir, "dbt_files",database_name)
    profiles_dir = dbt_dir  # profiles.yml is in dbt_files

    # Ensure seeds folder exists and copy CSV files from data folder
    seeds_folder = os.path.join(dbt_dir, "seeds")
    os.makedirs(seeds_folder, exist_ok=True)
    # Fix: Use repo root to find data folder
    repo_root = os.path.abspath(os.path.join(base_dir, "..", "..", "..", ".."))
    data_folder = os.path.join(repo_root, "data")
    if not os.path.isdir(data_folder):
        # Try relative to current file (for monorepo or alternate layouts)
        data_folder = os.path.abspath(os.path.join(base_dir, "..", "..", "data"))
    if os.path.isdir(data_folder):
        for filename in os.listdir(data_folder):
            if filename.endswith('.csv'):
                src = os.path.join(data_folder, filename)
                dst = os.path.join(seeds_folder, filename)
                shutil.copy2(src, dst)

    print("Running dbt seed...")
    run_dbt_seed(dbt_dir, profiles_dir)
    print("Running dbt run...")
    run_dbt_run(dbt_dir, profiles_dir)
    print("Running dbt test...")
    run_dbt_test(dbt_dir, profiles_dir)
    print("Generating dbt docs...")
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = profiles_dir
    subprocess.run("dbt docs generate", shell=True, cwd=dbt_dir, env=env)
    print("Opening dbt docs...")
    open_dbt_docs(dbt_dir, profiles_dir)

if __name__ == "__main__":
    execute_all('pubchem_compounds')

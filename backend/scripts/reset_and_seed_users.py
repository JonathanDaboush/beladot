import sys
import os
import asyncio

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'backend', 'scripts')

async def run_script(script_name: str) -> None:
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    env = os.environ.copy()
    env['PYTHONPATH'] = PROJECT_ROOT
    proc = await asyncio.create_subprocess_exec(
        sys.executable, script_path,
        env=env, cwd=PROJECT_ROOT
    )
    ret = await proc.wait()
    if ret != 0:
        print(f"Failed to run {script_name}")
        sys.exit(ret)

async def main() -> None:
    print("Clearing all users...")
    await run_script('clear_users.py')
    print("Seeding demo users...")
    await run_script('seed_demo_data.py')
    print("Done. Users table should be clean and seeded.")

if __name__ == "__main__":
    asyncio.run(main())

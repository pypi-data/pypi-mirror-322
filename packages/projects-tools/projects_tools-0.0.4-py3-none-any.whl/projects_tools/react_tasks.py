import subprocess
from .utils import console, print_section, print_command
from jinja2 import Environment, PackageLoader

# Initialize Jinja2 environment and rich console
env = Environment(
    loader=PackageLoader('projects_tools', 'templates')
)

def create_react_project(project_name, project_path):
    """Create React project with TypeScript"""
    try:
        # Render and write Makefile
        makefile_template = env.get_template('Makefile.jinja2')
        makefile_content = makefile_template.render(project_name=project_name, python_package_name=project_name.replace('-', '_'))
        with open(project_path / "Makefile", "w") as f:
            f.write(makefile_content)

        console.print(f"\n[bold yellow]Executing make reactjs (this may take a few minutes)...[/bold yellow]")
        process = subprocess.Popen(
            ['make', 'reactjs'],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                console.print(output.strip())
                
        return_code = process.poll()
        if return_code != 0:
            console.print(f"[red]make reactjs command failed with return code {return_code}[/red]")
            return False
            
        return True
    except Exception as e:
        console.print(f"[red]Error executing make reactjs: {str(e)}[/red]")
        return False
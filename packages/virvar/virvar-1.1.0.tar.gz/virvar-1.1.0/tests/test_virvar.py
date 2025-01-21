import pytest
import shutil
import sys
from virvar.virvar import main, virvar

@pytest.fixture
def create_fake_env(tmp_path):
    """
    Fixture to create a fake virtual environment with an activate file.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.

    Returns:Path
        Path: Path to the activate file of the virtual environment.
    """
    # Create the virtual environment path
    fake_env_path = tmp_path / "venv"

    # Path for POSIX-compliant systems (e.g., Linux, macOS, BSD)
    bin_path_unix = fake_env_path / "bin"
    bin_path_unix.mkdir(parents=True)

    #  Path for WINDOWS-compliant systems 
    bin_path_windows = fake_env_path / "Scripts"
    bin_path_windows.mkdir(parents=True)

    fake_message = """# Fake activate script
echo "Activating fake virtual environment"
# Self destruct!
"""

    # Create the activate files
    activate_file_unix = bin_path_unix / "activate"
    activate_file_unix.write_text(fake_message)

    activate_file_windows = bin_path_windows / "activate"
    activate_file_windows.write_text(fake_message)

    return activate_file_unix, activate_file_windows


def test_create_fake_env(create_fake_env):
    """
    Verify that the create_fake_env fixture creates a valid activate file
    for unix and windows environment.
    """
    for activate_file in create_fake_env:
        print(activate_file, activate_file.parent, activate_file.parent.parent)
        # Check that the activate file exists
        assert activate_file.exists(), f"The activate file for {activate_file} should exist after the fixture runs."
        
        # Check the initial content of the activate file
        content = activate_file.read_text()
        assert "# Fake activate script" in content, "The activate file in unix environment should contain the expected script header."
        assert "# Self destruct!" in content, "The activate file in unix environment should contain the self-destruct marker."


def test_virvar_adds_env_vars(create_fake_env):
    """
    Test that virvar adds environment variables to the activate file correctly
    for unix and windows environment.
    """

    # Example environment variables to add
    env_vars = {"TEST_VAR1": "test_value1", "TEST_VAR2": "test_value2"}

    for activate_file in create_fake_env:
        # Call the virvar function
        virvar(str(activate_file.parent.parent), **env_vars)


        # Read the updated activate file
        updated_content = activate_file.read_text()

        # Verify that export commands are added
        assert 'export TEST_VAR1="test_value1"' in updated_content, "TEST_VAR1 export is missing."
        assert 'export TEST_VAR2="test_value2"' in updated_content, "TEST_VAR2 export is missing."

        # Verify that unset commands are added in the correct place
        assert "unset TEST_VAR1" in updated_content, "TEST_VAR1 unset is missing."
        assert "unset TEST_VAR2" in updated_content, "TEST_VAR2 unset is missing."

        # Verify placement of unset commands
        self_destruct_index = updated_content.index("# Self destruct!")
        unset_index = updated_content.index("unset TEST_VAR1")
        assert unset_index > self_destruct_index, "Unset commands should come after the # Self destruct! marker."
        # Removes the fake virtual environment to ensure a complete reset before the next
        # iteration of the test loop for each environment (Unix and Windows).
        shutil.rmtree(activate_file.parent)


def test_main_no_arguments(monkeypatch, capsys):
    # Simule un appel sans argument 
    # argparse appelle par défaut sys.exit et lève une exception SystemExit
    monkeypatch.setattr(sys, "argv", ["virvar"])

    with pytest.raises(SystemExit) as excinfo: # Capture l'exception SystemExit 
        main()

    # Vérifie que le code de sortie est 2 (argparse le fait pour des erreurs)
    assert excinfo.value.code == 2 

    # Vérifie que le bon message d'erreur est affiché
    captured = capsys.readouterr()
    assert "the following arguments are required" in captured.err


def test_main_with_arguments(monkeypatch, capsys, create_fake_env):
    # Utilise la fixture pour créer un environement fictif pour environement unix
    # et windows
    for fake_activate_file in create_fake_env:
        fake_env_path = fake_activate_file.parent.parent # Récupére le chemin de l'environement
        # Simule un appel avec des arguments
        monkeypatch.setattr(sys, "argv", ["virvar", str(fake_env_path), "ENV_VAR=value"])

        # Vérifie que la fonction s'éxécute sans erreur et retourne le bon code
        assert main() is None

        # Capture et vérifie les sorties
        captured = capsys.readouterr()
        # Vérifie la sortie
        assert "Environment validated:" and "virtual environment detected, and environment variables successfully configured." in captured.out
        # Removes the fake virtual environment to ensure a complete reset before the next
        # iteration of the test loop for each environment (Unix and Windows).


def test_main_with_incorrect_path(monkeypatch, capsys, create_fake_env):

    # Simule un appel avec un mauvais chemin pour l'environment virtuel
    monkeypatch.setattr(sys, "argv", ["virvar", "path/to/incorrect_file", "ENV_VAR=value"])

    # Vérifie que FileNotFoundError est levée avec un message attendu
    with pytest.raises(FileNotFoundError) as excinfo:
        main()
    
    # Vérifie que le message d'erreur de l'exception
    assert "No such file or directory" in str(excinfo.value)

    # Capture et vérifie la sortie standard
    captured = capsys.readouterr()
    print(captured)
    assert "Error: Virtual environment not found. Unable to configure environment variables. Please ensure the specified path is correct." in captured.out


def test_variable_types_match(create_fake_env):
    # Récupérer le chemin du fichier activate depuis la fixture pour environement unix
    # et windows
    for activate_file in create_fake_env:
        fake_env_path = activate_file.parent.parent  # Revenir au chemin du dossier venv

        # Appeler la fonction virvar avec des variables de types différents
        virvar(
            str(fake_env_path),
            STRING_VAR="value",
            INT_VAR=123,
            FLOAT_VAR=45.67,
        )

        # Lire le contenu du fichier activate
        content = activate_file.read_text()

        # Extraire les variables définies dans le fichier
        variables = {
            line.split("=", 1)[0].replace("export ", "").strip(): eval(line.split("=", 1)[1].strip())
            for line in content.splitlines()
            if line.startswith("export ")
        }

        # Vérifier que les types correspondent
        assert variables["STRING_VAR"] == "value"
        assert variables["INT_VAR"] == 123
        assert variables["FLOAT_VAR"] == 45.67
        # Removes the fake virtual environment to ensure a complete reset before the next
        # iteration of the test loop for each environment (Unix and Windows).
        shutil.rmtree(activate_file.parent)

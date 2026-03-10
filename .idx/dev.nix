# dev.nix - Configuración del entorno de desarrollo para LeadLinked AI
# Incluye Python 3, Node.js 20 (para Appium), y Android tools (adb)

{ pkgs, ... }: {

  # Paquetes del sistema disponibles en el workspace
  packages = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.nodejs_20
    pkgs.android-tools
    pkgs.ffmpeg
    pkgs.pulseaudio
    pkgs.jdk17
    # --- Paquetes de Python ---
    pkgs.python3Packages.pydub
    pkgs.python3Packages.fastapi
    pkgs.python3Packages.uvicorn
    pkgs.python3Packages.python-multipart
  ];

  # Variables de entorno para persistencia del emulador y Java
  env = {
    ANDROID_USER_HOME = "$PWD/.android_data";
    ANDROID_AVD_HOME = "$PWD/.android_data/avd";
    JAVA_HOME = "${pkgs.jdk17}/lib/openjdk";
  };

  # Hooks del ciclo de vida del workspace
  idx = {
    # Se ejecuta cada vez que se inicia el workspace
    workspace = {
      onStart = {
        install-appium = ''
          # Instalar Appium globalmente via npm
          # Se instala una version especifica para evitar conflictos con nodejs
          npm i -g appium@2.5.1
          
          # Se elimina el directorio de drivers para evitar conflictos
          rm -rf ~/.appium

          # Instalar el driver UiAutomator2 para Android
          appium driver install uiautomator2@2.43.2
        '';
      };
    };

    # Extensiones de VS Code recomendadas
    extensions = [
      "ms-python.python"
    ];

    # Previews habilitados para cargar el Emulador de Android en IDX
    previews = {
      enable = true;
      previews = {
        android = {
          manager = "android";
        };
      };
    };
  };
}

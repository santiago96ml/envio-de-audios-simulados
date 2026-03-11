# dev.nix - Configuración del entorno de desarrollo para LeadLinked AI
# Incluye Python 3, Node.js 20 (para Appium), y Android tools (adb)

{ pkgs, ... }: {

  # 1. Paquetes del SISTEMA (Herramientas base)
  packages = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.nodejs_20
    pkgs.android-tools
    pkgs.ffmpeg
    pkgs.pulseaudio
    pkgs.pavucontrol
    pkgs.jdk17
  ];

  # 2. Variables de entorno
  env = {
    ANDROID_USER_HOME = "$PWD/.android_data";
    ANDROID_AVD_HOME = "$PWD/.android_data/avd";
    JAVA_HOME = "${pkgs.jdk17}/lib/openjdk";
    QEMU_AUDIO_DRV = "pa"; # Forzar audio a PulseAudio
  };

  idx = {
    workspace = {
      # onCreate se ejecuta solo la primera vez que se crea el proyecto
      onCreate = {
        # Instalamos todas las dependencias de Python via pip para evitar errores de Nix
        install-python-deps = "pip install appium-python-client fastapi uvicorn pydub python-multipart";
      };
      
      # onStart se ejecuta cada vez que abres el proyecto
      onStart = {
        install-appium = ''
          # Instalar Appium y el driver de Android
          npm i -g appium@2.5.1
          appium driver install uiautomator2@2.43.2 || true
        '';
      };
    };

    # Extensiones de VS Code
    extensions = [
      "ms-python.python"
    ];

    # Configuración del emulador de Android
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
name: Build APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - uses: actions/checkout@v4

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            build-essential git zip unzip \
            autoconf automake libtool pkg-config \
            libffi-dev libssl-dev zlib1g-dev \
            python3-dev

      - name: Clean Buildozer cache
        run: rm -rf .buildozer

      - name: Install Buildozer and Cython
        run: |
          pip install --user --upgrade "Cython<3.0" buildozer
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Build APK with Buildozer
        env:
          APP_ANDROID_ACCEPT_SDK_LICENSE: 1
        run: |
          buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: ndsn-debug-apk
          path: bin/*.apk

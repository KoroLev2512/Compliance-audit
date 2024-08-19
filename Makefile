PYTHON := python
SRC_DIR := src
TARGET := greedy_algo/greedy.py
JOBS := 4
OUTPUT_DIR := build

.PHONY: all
all: build

# didnt work, prefer to use build-pyinstaller
.PHONY: build
build-nuitka: $(SRC_DIR)/$(TARGET)
	@echo "Building $(TARGET) with Nuitka..."
	@$(PYTHON) -m nuitka --onefile --enable-plugin=tk-inter --noinclude-numba-mode=nofollow --jobs=$(JOBS) --output-dir=$(OUTPUT_DIR) $<

.PHONY: build-pyinstaller
build-pyinstaller: $(SRC_DIR)/$(TARGET)
	@echo "Building $(TARGET) with Pyinstaller..."
	@pyinstaller --noconsole --onefile --paths=$(PWD)/$(SRC_DIR)/ $<

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf $(OUTPUT_DIR)
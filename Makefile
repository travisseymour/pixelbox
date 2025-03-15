# NOTE: whitespace in front of commands are Tabs!
# Install the package with development dependencies
# alternative to `pip install -r requirements`
install:
	pip install -U pip wheel
	pip install .[dev] && pip uninstall pixelbox -y && make clean

# Clean up build artifacts
clean:
	rm -rf build/ dist/ *.egg-info

# Format the code
format:
	ruff check pixelbox --fix
	ruff format pixelbox
	black pixelbox

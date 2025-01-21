import setuptools

with open("README.md", 'r') as fin:
    long_desc = fin.read()

reqs = [
    "jinja2",
    "pygments",
    "markdown",
    "beautifulsoup4",
    "importlib_resources",
    "python_dateutil",
]

extras = {
    'test': [ "pytest" ],
    'expectations': [ "optimism>=2.7.5" ],
    'turtle_capture': [ "Pillow>=6.0.0" ], # note: also ghostscript!
    'synth': [ "wavesynth>=1.0.3" ],
    'server': [ "flask", "flask_cas", "redis" ],
    'security': [ "flask_talisman", "flask_seasurf" ],
    'https_debug': [ "pyopenssl" ],
    'formatting': [ "pymdown-extensions" ]
}

allExtras = []
for value in extras.values():
    allExtras.extend(value)

extras['all'] = allExtras

setuptools.setup(
    name="potluck-eval",
    version="1.2.36",
    requires=reqs,
    install_requires=reqs,
    extras_require=extras,
    python_requires=">=2.7", # actually requires 3.6 for most stuff!
    provides=["potluck", "potluck_server"],
    url="https://cs.wellesley.edu/~pmwh/potluck/docs/",
    description=(
        "Python code evaluation system and submissions server capable"
        " of unit tests, tracing, and AST inspection. Server can run on"
        " Python 2.7 but evaluation requires 3.7+."
    ),
    author="Peter Mawhorter",
    author_email="pmawhort@wellesley.edu",
    packages=["potluck", "potluck.tests", "potluck_server"],
    py_modules=["potluckDelivery"],
    include_package_data=True, # include data in packages that's in MANIFEST.in
    scripts=["scripts/potluck_eval", "scripts/potluck_tool"],
    # Note: MANIFEST.in handles package data
    license="BSD 3-Clause License",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Flask",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
    long_description=long_desc,
    long_description_content_type="text/markdown"
)

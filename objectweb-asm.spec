Name:		objectweb-asm
Version:	9.11.1
Release:	1
Summary:	Java bytecode manipulation framework
Group:		Development/Java
License:	BSD
URL:		https://asm.ow2.io/
%global asm_tag %(echo %{version} | tr '.' '_')
Source0:	https://gitlab.ow2.org/asm/asm/-/archive/ASM_%{asm_tag}/asm-ASM_%{asm_tag}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildSystem:	maven

%description
ASM is a Java bytecode analysis and manipulation framework.

%prep
%setup -q -n asm-ASM_%{asm_tag}
# Gradle would download its wrapper. These modules are plain Java.
# Release 11 matches upstream sourceCompatibility.
python - %{version} <<'PY'
import sys
from pathlib import Path

version = sys.argv[1]
modules = [
    ("asm", []),
    ("asm-tree", ["asm"]),
    ("asm-analysis", ["asm-tree"]),
    ("asm-commons", ["asm", "asm-tree"]),
    ("asm-util", ["asm", "asm-tree", "asm-analysis"]),
]
names = "\n".join(f"    <module>{name}</module>" for name, _deps in modules)
Path("pom.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.ow2.asm</groupId>
  <artifactId>asm-parent</artifactId>
  <version>{version}</version>
  <packaging>pom</packaging>
  <name>ASM</name>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>11</maven.compiler.release>
  </properties>
  <modules>
{names}
  </modules>
</project>
""")
for name, deps in modules:
    body = ""
    if deps:
        lines = []
        for dep in deps:
            lines.append(f"""    <dependency>
      <groupId>org.ow2.asm</groupId>
      <artifactId>{dep}</artifactId>
      <version>{version}</version>
    </dependency>""")
        body = "  <dependencies>\n" + "\n".join(lines) + "\n  </dependencies>\n"
    Path(name, "pom.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<project>
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm-parent</artifactId>
    <version>{version}</version>
  </parent>
  <artifactId>{name}</artifactId>
  <name>{name}</name>
{body}</project>
""")
PY

%files -f .mfiles
%doc LICENSE.txt README.md

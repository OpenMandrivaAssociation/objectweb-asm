Name:		objectweb-asm
Version:	9.11.1
Release:	2
Summary:	Java bytecode manipulation framework
Group:		Development/Java
License:	BSD
URL:		https://asm.ow2.io/
%global asm_tag %(echo %{version} | tr '.' '_')
Source0:	https://gitlab.ow2.org/asm/asm/-/archive/ASM_%{asm_tag}/asm-ASM_%{asm_tag}.tar.gz
# Gradle 9.9.1 strictly pins 9.10.1. Class files shipped as test
# fixtures are removed from this archive before it is stored.
Source1:	https://gitlab.ow2.org/asm/asm/-/archive/ASM_9_10_1/asm-ASM_9_10_1.tar.gz
BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

%description
ASM is a Java bytecode analysis and manipulation framework.
9.11.1 stays the default jar. Gradle 9.9.1 strictly pins 9.10.1
for asm, asm-commons, and asm-tree, so those jars are installed
beside it.

%prep
%setup -q -n asm-ASM_%{asm_tag}
%setup -q -T -D -a 1 -n asm-ASM_%{asm_tag}
find asm-ASM_9_10_1 \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete
# Gradle build files pull sigtest and janino. The Maven poms written
# below are what this package builds, including the nested 9.10.1 tree.
rm -f build.gradle settings.gradle
rm -f asm-ASM_9_10_1/build.gradle asm-ASM_9_10_1/settings.gradle
find asm-ASM_9_10_1 -name pom.xml -delete
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

%build -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cp=
for mod in asm asm-tree asm-commons; do
	mkdir -p "asm910/$mod"
	find "asm-ASM_9_10_1/$mod/src/main/java" -name '*.java' ! -name 'module-info.java' > "asm910/$mod.list"
	test -s "asm910/$mod.list"
	if [ -n "$cp" ]; then
		"$JAVA_HOME/bin/javac" --release 11 -encoding UTF-8 -Xlint:-options \
			-cp "$cp" -d "asm910/$mod" @"asm910/$mod.list"
	else
		"$JAVA_HOME/bin/javac" --release 11 -encoding UTF-8 -Xlint:-options \
			-d "asm910/$mod" @"asm910/$mod.list"
	fi
	"$JAVA_HOME/bin/jar" cf "asm910/$mod.jar" -C "asm910/$mod" .
	cat > "asm910/$mod.pom" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.ow2.asm</groupId>
  <artifactId>$mod</artifactId>
  <version>9.10.1</version>
  <name>$mod</name>
  <description>ASM $mod 9.10.1</description>
  <url>https://asm.ow2.io/</url>
  <licenses>
    <license>
      <name>BSD-3-Clause</name>
      <url>https://asm.ow2.io/license.html</url>
    </license>
  </licenses>
</project>
EOF
	if [ -z "$cp" ]; then
		cp="asm910/$mod.jar"
	else
		cp="$cp:asm910/$mod.jar"
	fi
done

%install -p
: > .mfiles910
for mod in asm asm-tree asm-commons; do
	sysjar install --buildroot %{buildroot} \
		--artifact "asm910/$mod.pom:asm910/$mod.jar" \
		--file-name "$mod-9.10.1" \
		--filelist ".mfiles910-$mod"
	/bin/mv %{buildroot}/usr/share/sysjar/index/org.ow2.asm/$mod.sysjar \
		%{buildroot}/usr/share/sysjar/index/org.ow2.asm/$mod-9.10.1.sysjar
	sed -i "s|/usr/share/sysjar/index/org.ow2.asm/${mod}\\.sysjar|/usr/share/sysjar/index/org.ow2.asm/${mod}-9.10.1.sysjar|" ".mfiles910-$mod"
	while IFS= read -r line; do
		grep -qxF -- "$line" .mfiles910 || printf '%s\n' "$line" >> .mfiles910
	done < ".mfiles910-$mod"
done

%install -a
while IFS= read -r line; do
	grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
done < .mfiles910

%check -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cat > AsmSmoke.java << 'EOF'
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.ClassNode;
import org.objectweb.asm.commons.Method;
public class AsmSmoke {
	public static void main(String[] args) {
		ClassWriter writer = new ClassWriter(0);
		writer.visit(Opcodes.V1_8, Opcodes.ACC_PUBLIC, "T", null, "java/lang/Object", null);
		writer.visitEnd();
		int length = writer.toByteArray().length;
		if (length < 10) {
			throw new AssertionError(length);
		}
		ClassNode node = new ClassNode();
		node.name = "T";
		Method method = Method.getMethod("void main(String[])");
		if (!"main".equals(method.getName()) || !"T".equals(node.name)) {
			throw new AssertionError(method.getName());
		}
		System.out.println(args[0] + " " + node.name + " " + method.getName());
	}
}
EOF
newcp="%{buildroot}%{_javadir}/asm.jar:%{buildroot}%{_javadir}/asm-tree.jar:%{buildroot}%{_javadir}/asm-commons.jar"
oldcp="%{buildroot}%{_javadir}/asm-9.10.1.jar:%{buildroot}%{_javadir}/asm-tree-9.10.1.jar:%{buildroot}%{_javadir}/asm-commons-9.10.1.jar"
"$JAVA_HOME/bin/javac" --release 11 -encoding UTF-8 -Xlint:-options -cp "$newcp" AsmSmoke.java
"$JAVA_HOME/bin/java" -cp "$newcp:." AsmSmoke asm911_ok > check911.log
cat check911.log
grep -F -q 'asm911_ok T main' check911.log
"$JAVA_HOME/bin/javac" --release 11 -encoding UTF-8 -Xlint:-options -cp "$oldcp" AsmSmoke.java
"$JAVA_HOME/bin/java" -cp "$oldcp:." AsmSmoke asm910_ok > check910.log
cat check910.log
grep -F -q 'asm910_ok T main' check910.log

%files -f .mfiles
%doc LICENSE.txt README.md

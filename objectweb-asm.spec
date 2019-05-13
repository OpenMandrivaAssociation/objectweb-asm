Name:           objectweb-asm
Version:        7.1
Release:        3
Summary:        Java bytecode manipulation and analysis framework
License:        BSD
URL:            http://asm.ow2.org/
BuildArch:      noarch
BuildRequires:	jdk-current
BuildRequires:	javapackages-local

Source0:        https://repository.ow2.org/nexus/content/repositories/releases/org/ow2/asm/asm/%{version}/asm-%{version}-sources.jar
Source1:        https://repository.ow2.org/nexus/content/repositories/releases/org/ow2/asm/asm/%{version}/asm-%{version}.pom

%description
ASM is an all purpose Java bytecode manipulation and analysis
framework.  It can be used to modify existing classes or dynamically
generate classes, directly in binary form.  Provided common
transformations and analysis algorithms allow to easily assemble
custom complex transformations and code analysis tools.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
This package provides %{summary}.

%prep
%autosetup -p1 -c asm-%{version}

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

cat >module-info.java <<'EOF'
module org.objectweb.asm {
	exports org.objectweb.asm;
	exports org.objectweb.asm.signature;
}
EOF
find . -name "*.java" |xargs javac
javadoc -d docs -sourcepath . org.objectweb.asm
find . -name "*.java" |xargs rm -f
jar cf asm-%{version}.jar META-INF org module-info.class
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp asm-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap asm-%{version}.pom asm-%{version}.jar
cp -a docs %{buildroot}%{_javadocdir}/org.objectweb.asm
mv %{buildroot}%{_javadir}/*.jar %{buildroot}%{_javadir}/modules/
ln -s modules/asm-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/asm-%{version}.jar %{buildroot}%{_javadir}/asm.jar
ln -s modules/asm-%{version}.jar %{buildroot}%{_javadir}/org.objectweb.asm.jar

%files -f .mfiles
%{_javadir}/*.jar
%{_javadir}/modules/*.jar

%files javadoc
%{_javadocdir}/org.objectweb.asm

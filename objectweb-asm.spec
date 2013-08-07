# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free

Summary:	A code manipulation tool to implement adaptable systems
Name:		objectweb-asm
Version:	3.1
Release:	0.5.2
License:	BSD
Url:		http://asm.objectweb.org/
Group:		Development/Java
Source0:	http://download.forge.objectweb.org/asm/asm-3.1.tar.gz
Source1:	http://repo1.maven.org/maven2/asm/asm/3.1/asm-3.1.pom
Source2:	http://repo1.maven.org/maven2/asm/asm-analysis/3.1/asm-analysis-3.1.pom
Source3:	http://repo1.maven.org/maven2/asm/asm-commons/3.1/asm-commons-3.1.pom
Source4:	http://repo1.maven.org/maven2/asm/asm-tree/3.1/asm-tree-3.1.pom
Source5:	http://repo1.maven.org/maven2/asm/asm-util/3.1/asm-util-3.1.pom
Source6:	http://repo1.maven.org/maven2/asm/asm-xml/3.1/asm-xml-3.1.pom
Source7:	http://repo1.maven.org/maven2/asm/asm-all/3.1/asm-all-3.1.pom
Source8:	http://repo1.maven.org/maven2/asm/asm-parent/3.1/asm-parent-3.1.pom
Source9:	asm-MANIFEST.MF
Patch0:		objectweb-asm-no-classpath-in-manifest.patch
BuildArch:	noarch
BuildRequires:	jpackage-utils >= 0:1.7.4
BuildRequires:	java-devel >= 0:1.5.0
BuildRequires:	ant >= 0:1.6.5
BuildRequires:	objectweb-anttask
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:	zip
# Needed by asm-xml.jar
Requires:	xml-commons-jaxp-1.3-apis
Requires(post,postun):	jpackage-utils >= 0:1.7.4

%description
ASM is a code manipulation tool to implement adaptable systems.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
Javadoc for %{name}.

%prep
%setup -qn asm-%{version}
%patch0 -p1
perl -pi -e 's/\r$//g' LICENSE.txt README.txt

mkdir META-INF
cp -p %{SOURCE9} META-INF/MANIFEST.MF

%build
export CLASSPATH=
export OPT_JAR_LIST=:
ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}

for jar in output/dist/lib/*.jar; do
install -m 644 ${jar} \
%{buildroot}%{_javadir}/%{name}/`basename ${jar}`
done

touch META-INF/MANIFEST.MF
zip -u output/dist/lib/all/asm-all-%{version}.jar META-INF/MANIFEST.MF

install -m 644 output/dist/lib/all/asm-all-%{version}.jar %{buildroot}%{_javadir}/%{name}/

(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# pom
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm.pom
%add_to_maven_depmap org.objectweb.asm asm %{version} JPP/objectweb-asm asm
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-analysis.pom
%add_to_maven_depmap org.objectweb.asm asm-analysis %{version} JPP/objectweb-asm asm-analysis
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-commons.pom
%add_to_maven_depmap org.objectweb.asm asm-commons %{version} JPP/objectweb-asm asm-commons
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-tree.pom
%add_to_maven_depmap org.objectweb.asm asm-tree %{version} JPP/objectweb-asm asm-tree
install -m 644 %{SOURCE5} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-util.pom
%add_to_maven_depmap org.objectweb.asm asm-util %{version} JPP/objectweb-asm asm-util
install -m 644 %{SOURCE6} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-xml.pom
%add_to_maven_depmap org.objectweb.asm asm-xml %{version} JPP/objectweb-asm asm-xml
install -m 644 %{SOURCE7} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-all.pom
%add_to_maven_depmap org.objectweb.asm asm-all %{version} JPP/objectweb-asm asm-all
install -m 644 %{SOURCE8} %{buildroot}%{_datadir}/maven2/poms/JPP.objectweb-asm-asm-parent.pom
%add_to_maven_depmap org.objectweb.asm asm-parent %{version} JPP/objectweb-asm asm-parent

# javadoc
install -p -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/user/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


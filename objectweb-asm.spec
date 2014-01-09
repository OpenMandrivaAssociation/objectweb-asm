%{?_javapackages_macros:%_javapackages_macros}
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

Name:           objectweb-asm
Version:        3.3.1
Release:        8.1%{?dist}
Epoch:          0
Summary:        A code manipulation tool to implement adaptable systems
License:        BSD
URL:            http://asm.objectweb.org/

Source0:        http://download.forge.objectweb.org/asm/asm-3.3.1.tar.gz
Source1:        asm-MANIFEST.MF
Patch0:         objectweb-asm-no-classpath-in-manifest.patch
# Needed by asm-xml.jar
Requires:       xml-commons-jaxp-1.3-apis
Requires(post): jpackage-utils >= 0:1.7.4
Requires(postun): jpackage-utils >= 0:1.7.4
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  objectweb-anttask
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  zip
BuildArch:      noarch

%description
ASM is a code manipulation tool to implement adaptable systems.

%package        javadoc
Summary:        Javadoc for %{name}


%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n asm-%{version}
%patch0 -p1
perl -pi -e 's/\r$//g' LICENSE.txt README.txt

mkdir META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF

%build
ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

for jar in output/dist/lib/*.jar; do
install -m 644 ${jar} \
$RPM_BUILD_ROOT%{_javadir}/%{name}/`basename ${jar/-%{version}/}`
done

touch META-INF/MANIFEST.MF
zip -u output/dist/lib/all/asm-all-%{version}.jar META-INF/MANIFEST.MF

install -m 644 output/dist/lib/all/asm-all-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/asm-all.jar
install -m 644 output/dist/lib/all/asm-all-%{version}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.objectweb-asm-asm-all.pom

# pom
for pom in output/dist/lib/*.pom; do
install -m 644 ${pom} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.objectweb-asm-`basename ${pom/-%{version}/}`
done
%add_maven_depmap JPP.objectweb-asm-asm.pom %{name}/asm.jar
%add_maven_depmap JPP.objectweb-asm-asm-analysis.pom %{name}/asm-analysis.jar
%add_maven_depmap JPP.objectweb-asm-asm-commons.pom %{name}/asm-commons.jar
%add_maven_depmap JPP.objectweb-asm-asm-tree.pom %{name}/asm-tree.jar
%add_maven_depmap JPP.objectweb-asm-asm-util.pom %{name}/asm-util.jar
%add_maven_depmap JPP.objectweb-asm-asm-xml.pom %{name}/asm-xml.jar
%add_maven_depmap JPP.objectweb-asm-asm-all.pom %{name}/asm-all.jar -a "org.eclipse.jetty.orbit:org.objectweb.asm"
%add_maven_depmap JPP.objectweb-asm-asm-parent.pom

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr output/dist/doc/javadoc/user/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-7
- Make jetty orbit depmap point to asm-all jar
- Resolves: rhbz#917625

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-6
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#917625

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 0:3.3.1-2
- Use poms produced by the build not foreign ones.
- Adpat to current guidelines.

* Mon Apr 04 2011 Chris Aniszczyk <zx@redhat.com> 0:3.3.1
- Upgrade to 3.3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com>  0:3.2.1-2
- Change depmap parent id to asm (bug #606659)

* Thu Apr 15 2010 Fernando Nasser <fnasser@redhat.com> 0:3.2.1
- Upgrade to 3.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5.1
- build for Fedora

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5
- add OSGi manifest (Alexander Kurtakov)

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:3.1-4
- remove Class-Path from MANIFEST.MF
- add unversioned javadoc symlink
- remove javadoc scriptlets
- fix directory ownership
- remove build requirement on dos2unix

* Fri Feb 08 2008 Ralph Apel <r.apel@r-apel.de> - 0:3.1-3jpp
- Add poms and depmap frags with groupId of org.objectweb.asm !
- Add asm-all.jar 
- Add -javadoc Requires post and postun
- Restore Vendor, Distribution

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-2jpp
- Fix EOL of txt files
- Add dependency on jaxp 

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-1jpp
- Upgrade to 3.1

* Wed Aug 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.0-1jpp
- Upgrade to 3.0
- Rename to include objectweb- prefix as requested by ObjectWeb

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.1-2jpp
- First JPP 1.7 build

* Thu Oct 06 2005 Ralph Apel <r.apel at r-apel.de> 0:2.1-1jpp
- Upgrade to 2.1

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:2.0.RC1-1jpp
- First release of the 2.0 line.

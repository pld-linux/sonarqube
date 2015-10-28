# TODO
# - build it from sources
%include	/usr/lib/rpm/macros.java
Summary:	Open platform to manage code quality
Name:		sonarqube
# Stick to LTS version
Version:	4.5.6
Release:	0.1
License:	LGPL v3
Group:		Networking/Daemons/Java/Servlets
Source0:	https://sonarsource.bintray.com/Distribution/sonarqube/%{name}-%{version}.zip
# Source0-md5:	3b372503944e1b21138d605d85cbf025
Source1:	context.xml
URL:		http://www.sonarqube.org/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.546
BuildRequires:	unzip
Requires:	java-servlet-container
Requires:	jpackage-utils
Obsoletes:	sonar < 4.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir %{_datadir}/%{name}

%description
SonarQube is an open source quality management platform, dedicated to
continuously analyze and measure source code quality, from the
portfolio to the method.

%prep
%setup -q

# other platform files
rm -r bin/linux-ppc-64
rm -r bin/macosx-*
rm -r bin/solaris-*
rm -r bin/windows-*

%ifnarch %{ix86}
rm -r bin/linux-x86-32
%endif
%ifnarch %{x8664}
rm -r bin/linux-x86-64
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_tomcatconfdir},%{_appdir},%{_sharedstatedir}/%{name}}
cp -a bin extensions lib web $RPM_BUILD_ROOT%{_appdir}
cp -a conf/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -s %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.properties
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.xml
%{_tomcatconfdir}/%{name}.xml
%{_datadir}/%{name}
%attr(755,tomcat,tomcat) %dir %{_sharedstatedir}/%{name}

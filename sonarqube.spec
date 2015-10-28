# TODO
# - build it from sources
%include	/usr/lib/rpm/macros.java
Summary:	Open platform to manage code quality
Name:		sonarqube
Version:	1.6
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons/Java/Servlets
Source0:	http://dist.sonar.codehaus.org/%{name}-%{version}.zip
# Source0-md5:	accde4b27b491e63fdba3995759162f5
Source1:	context.xml
URL:		http://www.sonarqube.org/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	java-servlet-container
Requires:	jpackage-utils
Obsoletes:	sonar
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SonarQube is an open source quality management platform, dedicated to
continuously analyze and measure source code quality, from the
portfolio to the method.

%prep
%setup -q

%build
cd war
%ant clean war

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir}/%{name},%{_sharedstatedir}/{%{name},tomcat/conf/Catalina/localhost}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/%{name}.xml
cp -a war/build/sonar-web/* $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/%{name}.xml
%{_datadir}/%{name}
%attr(755,tomcat,tomcat) %dir %{_sharedstatedir}/%{name}

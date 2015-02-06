Name:           ldm
Version:        2.1
Release:        2
Summary:        LTSP Display Manager

Group:          System/X11
License:        GPLv2+
URL:            https://code.launchpad.net/~ltsp-upstream/ltsp/ldm-trunk
Source0:        http://ftp.de.debian.org/debian/pool/main/l/ldm/%{name}_%{version}.orig.tar.gz


BuildRequires:  pkgconfig(gdk-2.0)
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  pkgconfig(iso-codes)

Requires:       netcat-traditional
Requires:       openssh-clients

%description
LTSP Display Manager handles network logins for remote desktop sessions.

%package -n ldminfod
Summary:        LTSP client
Group:          System/X11
Requires:       openssh-server

%description -n ldminfod
Provides Linux Terminal Server capabilities to the LDM client.

%prep
%setup -q


%build
%configure
%make


%install
%make DESTDIR=%{buildroot} install
#cd $RPM_BUILD_ROOT/%{_datadir}/ldm/themes
#    tar xfvj %SOURCE1
#    mv k12linux-theme-%{theme_version} k12linux
#    ln -s k12linux default
#cd -

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/ldm/

%find_lang ldm
%find_lang ldmrc 
%find_lang ltsp-cluster-info 
cat ltsp-cluster-info.lang ldmrc.lang >> ldm.lang

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/
install -m 0755 ldminfod/ldminfod $RPM_BUILD_ROOT%{_sbindir}/ldminfod
install -m 0644 ldminfod/xinetd.d/ldminfod $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/ldminfod

rm -rf $RPM_BUILD_ROOT%{_datadir}/ldm/themes/ltsp

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ltsp
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/ldm-global-dmrc <<EOL
[Desktop]
#Session=gnome
#Session=kde
#Session=xfce4
#Session=sugar
#Language=ja_JP.utf8
#Language=en_US.utf8
EOL
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/ldm-global-dmrc


%files -f ldm.lang
%doc COPYING README
%{_bindir}/ldm-dialog
%{_sbindir}/ldm
%{_libexecdir}/ldm/
%{_datadir}/ldm/
%{_mandir}/man1/ldm.1.xz
%{_datadir}/ltsp/screen.d/ldm
%dir %{_localstatedir}/run/ldm/

%files -n ldminfod
%doc COPYING README
%{_sbindir}/ldminfod
%config(noreplace) %{_sysconfdir}/xinetd.d/ldminfod
%config(noreplace) %{_sysconfdir}/ltsp/ldm-global-dmrc



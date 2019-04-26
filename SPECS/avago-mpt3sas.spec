%define vendor_name Avago
%define vendor_label avago
%define driver_name mpt3sas

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 27.101.00.00
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-avago-mpt3sas/archive?at=27.101.00.00&format=tgz&prefix=driver-avago-mpt3sas-27.101.00.00#/avago-mpt3sas-27.101.00.00.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-avago-mpt3sas/archive?at=27.101.00.00&format=tgz&prefix=driver-avago-mpt3sas-27.101.00.00#/avago-mpt3sas-27.101.00.00.tar.gz) = bc3814c01659a34ce3edb837ca3c22eb4b7eb657


BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__install} -d %{buildroot}%{_sysconfdir}/modprobe.d
echo 'options mpt3sas prot_mask=0x07' > %{driver_name}.conf
%{__install} %{driver_name}.conf %{buildroot}%{_sysconfdir}/modprobe.d
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Tue Dec 18 2018 Deli Zhang <deli.zhang@citrix.com> - 27.101.00.00-1
- CP-30072: Upgrade avago-mpt3sas driver to version 27.101.00.00

* Wed Oct 11 2017 Thomas Mckelvey <thomas.mckelvey@citrix.com> - 22.00.00.00-2
- CA-267947: Disabling DIX by setting prot_mask=0x07


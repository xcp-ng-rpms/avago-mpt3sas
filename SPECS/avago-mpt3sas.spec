%global package_speccommit 5e1bc03f03414290f5939dd29cfedfe610fa8b36
%global package_srccommit 38.00.00.00
%define vendor_name Avago
%define vendor_label avago
%define driver_name mpt3sas

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 38.00.00.00
Release: 1%{?xsrel}%{?dist}
License: GPL
Source0: avago-mpt3sas-38.00.00.00.tar.gz

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__install} -d %{buildroot}%{_sysconfdir}/modprobe.d
echo 'options mpt3sas prot_mask=0x07' > %{driver_name}.conf
%{__install} %{driver_name}.conf %{buildroot}%{_sysconfdir}/modprobe.d
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Mon Sep 05 2022 Zhuangxuan Fei <zhuangxuan.fei@citrix.com> - 38.00.00.00-1
- CP-40165: Upgrade avago-mpt3sas driver to version 38.00.00.00

* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 33.100.00.00-2
- CP-38416: Enable static analysis

* Wed May 20 2020 Tim Smith <tim.smith@citrix.com> - 33.100.00.00-1
- CP-34008 Update avago-mpt3sas driver to 33.100.00.00-1

* Tue Dec 18 2018 Deli Zhang <deli.zhang@citrix.com> - 27.101.00.00-1
- CP-30072: Upgrade avago-mpt3sas driver to version 27.101.00.00

* Wed Oct 11 2017 Thomas Mckelvey <thomas.mckelvey@citrix.com> - 22.00.00.00-2
- CA-267947: Disabling DIX by setting prot_mask=0x07



#
# Copyright (C) 1994-2018 Altair Engineering, Inc.
# For more information, contact Altair at www.altair.com.
#
# This file is part of the PBS Professional ("PBS Pro") software.
#
# Open Source License Information:
#
# PBS Pro is free software. You can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PBS Pro is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Commercial License Information:
#
# For a copy of the commercial license terms and conditions,
# go to: (http://www.pbspro.com/UserArea/agreement.html)
# or contact the Altair Legal Department.
#
# Altair’s dual-license business model allows companies, individuals, and
# organizations to create proprietary derivative works of PBS Pro and
# distribute them - whether embedded or bundled with other software -
# under a commercial license agreement.
#
# Use of Altair’s trademarks, including but not limited to "PBS™",
# "PBS Professional®", and "PBS Pro™" and Altair’s logos is subject to Altair's
# trademark licensing policies.
#

%if !%{defined pbs_name}
%define pbs_name pbspro
%endif

%if !%{defined pbs_version}
%define pbs_version 19.0.0
%endif

%if !%{defined pbs_release}
%define pbs_release 0
%endif

%if !%{defined pbs_prefix}
%define pbs_prefix /opt/pbs
%endif

%if !%{defined pbs_home}
%define pbs_home /var/spool/pbs
%endif

%if !%{defined pbs_dbuser}
%define pbs_dbuser postgres
%endif

%define pbs_client client
%define pbs_execution execution
%define pbs_server server
%define pbs_dist %{pbs_name}-%{pbs_version}.tar.gz

%if !%{defined _unitdir}
%define _unitdir /usr/lib/systemd/system
%endif
%if 0%{?suse_version} >= 1210 || 0%{?rhel} >= 7 || 0%{?debian_version} >= 8
%define have_systemd 1
%endif

Name: %{pbs_name}
Version: %{pbs_version}
Release: %{pbs_release}
Source0: %{pbs_dist}
%if 0%{?opensuse_bs}
%if %{defined suse_version}
Source1: %{name}-rpmlintrc
%endif
%endif
Summary: PBS Professional
License: AGPLv3 with exceptions
URL: http://www.pbspro.org
Vendor: Altair Engineering, Inc.
Prefix: %{?pbs_prefix}%{!?pbs_prefix:%{_prefix}}

%bcond_with alps
%bcond_with cpuset
%bcond_with ibm-ib
%bcond_with ibm-hps

BuildRoot: %{buildroot}
BuildRequires: gcc
BuildRequires: make
BuildRequires: rpm-build
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: hwloc-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libedit-devel
BuildRequires: libical-devel
BuildRequires: ncurses-devel
BuildRequires: perl
BuildRequires: postgresql-devel
BuildRequires: python-devel >= 2.6
BuildRequires: python-devel < 3.0
BuildRequires: tcl-devel
BuildRequires: tk-devel
BuildRequires: swig
%if %{defined suse_version}
BuildRequires: libexpat-devel
BuildRequires: libopenssl-devel
BuildRequires: libXext-devel
BuildRequires: libXft-devel
BuildRequires: fontconfig
BuildRequires: timezone
BuildRequires: python-xml
%else
BuildRequires: expat-devel
BuildRequires: openssl-devel
BuildRequires: libXext
BuildRequires: libXft
%endif

# Pure python extensions use the 32 bit library path
%{!?py_site_pkg_32: %global py_site_pkg_32 %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
%{!?py_site_pkg_64: %global py_site_pkg_64 %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

%package %{pbs_server}
Summary: PBS Professional for a server host
Group: System/Base
Conflicts: pbspro-execution
Conflicts: pbspro-client
Conflicts: pbspro-client-ohpc
Conflicts: pbspro-execution-ohpc
Conflicts: pbspro-server-ohpc
Conflicts: pbs
Conflicts: pbs-mom
Conflicts: pbs-cmds
Requires: bash
Requires: expat
Requires: libedit
Requires: postgresql-server
Requires: python >= 2.6
Requires: python < 3.0
Requires: tcl
Requires: tk
%if %{defined suse_version}
Requires: smtp_daemon
%if %{suse_version} >= 1500
Requires: libical3
%else
Requires: libical1
%endif
%else
Requires: smtpdaemon
Requires: libical
%endif
Autoreq: 1

%description %{pbs_server}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

This package is intended for a server host. It includes all
PBS Professional components.

%package %{pbs_execution}
Summary: PBS Professional for an execution host
Group: System/Base
Conflicts: pbspro-server
Conflicts: pbspro-client
Conflicts: pbspro-client-ohpc
Conflicts: pbspro-execution-ohpc
Conflicts: pbspro-server-ohpc
Conflicts: pbs
Conflicts: pbs-mom
Conflicts: pbs-cmds
Requires: bash
Requires: expat
Requires: python >= 2.6
Requires: python < 3.0
Autoreq: 1

%description %{pbs_execution}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

This package is intended for an execution host. It does not
include the scheduler, server, or communication agent. It
does include the PBS Professional user commands.

%package %{pbs_client}
Summary: PBS Professional for a client host
Group: System/Base
Conflicts: pbspro-server
Conflicts: pbspro-execution
Conflicts: pbspro-client-ohpc
Conflicts: pbspro-execution-ohpc
Conflicts: pbspro-server-ohpc
Conflicts: pbs
Conflicts: pbs-mom
Conflicts: pbs-cmds
Requires: bash
Requires: python >= 2.6
Requires: python < 3.0
Autoreq: 1

%description %{pbs_client}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

This package is intended for a client host and provides
the PBS Professional user commands.

%if 0%{?opensuse_bs}
# Do not specify debug_package for OBS builds.
%else
%if %{defined suse_version}
%debug_package
%endif
%endif

%prep
%setup

%build
[ -d build ] && rm -rf build
mkdir build
cd build
../configure \
	PBS_VERSION=%{pbs_version} \
	--prefix=%{pbs_prefix} \
%if %{defined suse_version}
	--libexecdir=%{pbs_prefix}/libexec \
%endif
%if %{with alps}
	--enable-alps \
%endif
%if %{with cpuset}
	--enable-cpuset \
%endif
%if %{with ibm-hps}
	--enable-hps \
%endif
%if %{with ibm-ib}
	--enable-aixib \
%endif
	--with-pbs-server-home=%{pbs_home} \
	--with-database-user=%{pbs_dbuser}
%{__make} %{?_smp_mflags}

%install
cd build
%make_install

%post %{pbs_server}
# do not run pbs_postinstall when the CLE is greater than or equal to 6
imps=0
cle_release_version=0
cle_release_path=/etc/opt/cray/release/cle-release
if [ -f ${cle_release_path} ]; then
        cle_release_version=`grep RELEASE ${cle_release_path} | cut -f2 -d= | cut -f1 -d.`
fi
[ "${cle_release_version}" -ge 6 ] 2>/dev/null && imps=1
if [ $imps -eq 0 ]; then
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_postinstall server \
	%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{pbs_home} %{pbs_dbuser}
else
        install -D %{pbs_prefix}/libexec/pbs_init.d /etc/init.d/pbs
fi

%post %{pbs_execution}
# do not run pbs_postinstall when the CLE is greater than or equal to 6
imps=0
cle_release_version=0
cle_release_path=/etc/opt/cray/release/cle-release
if [ -f ${cle_release_path} ]; then
        cle_release_version=`grep RELEASE ${cle_release_path} | cut -f2 -d= | cut -f1 -d.`
fi
[ "${cle_release_version}" -ge 6 ] 2>/dev/null && imps=1
if [ $imps -eq 0 ]; then
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_postinstall execution \
	%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{pbs_home}
else
        install -D %{pbs_prefix}/libexec/pbs_init.d /etc/init.d/pbs
fi

%post %{pbs_client}
# do not run pbs_postinstall when the CLE is greater than or equal to 6
imps=0
cle_release_version=0
cle_release_path=/etc/opt/cray/release/cle-release
if [ -f ${cle_release_path} ]; then
        cle_release_version=`grep RELEASE ${cle_release_path} | cut -f2 -d= | cut -f1 -d.`
fi
[ "${cle_release_version}" -ge 6 ] 2>/dev/null && imps=1
if [ $imps -eq 0 ]; then
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_postinstall client \
	%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}
else
        install -D %{pbs_prefix}/libexec/pbs_init.d /etc/init.d/pbs
fi

%preun %{pbs_server}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	[ -x /etc/init.d/pbs ] && /etc/init.d/pbs stop
	[ -x /sbin/chkconfig ] && /sbin/chkconfig --del pbs >/dev/null 2>&1
	rm -f /etc/rc.d/rc?.d/[KS]??pbs
	if [ `basename ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}` = %{version} ]; then
		top_level=`dirname ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}`
		if [ -h $top_level/default ]; then
			link_target=`readlink $top_level/default`
			[ `basename "$link_target"` = %{version} ] && rm -f $top_level/default
		fi
	fi
	rm -f /etc/init.d/pbs
	rm -f /opt/modulefiles/pbs/%{version}
	%if %{defined have_systemd}
		systemctl disable pbs
		rm -f /usr/lib/systemd/system-preset/95-pbs.preset
	%endif
fi

%preun %{pbs_execution}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	[ -x /etc/init.d/pbs ] && /etc/init.d/pbs stop
	[ -x /sbin/chkconfig ] && /sbin/chkconfig --del pbs >/dev/null 2>&1
	rm -f /etc/rc.d/rc?.d/[KS]??pbs
	if [ `basename ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}` = %{version} ]; then
		top_level=`dirname ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}`
		if [ -h $top_level/default ]; then
			link_target=`readlink $top_level/default`
			[ `basename "$link_target"` = %{version} ] && rm -f $top_level/default
		fi
	fi
	rm -f /etc/init.d/pbs
	rm -f /opt/modulefiles/pbs/%{version}
	%if %{defined have_systemd}
		systemctl disable pbs
		rm -f /usr/lib/systemd/system-preset/95-pbs.preset
	%endif
fi

%preun %{pbs_client}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	if [ `basename ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}` = %{version} ]; then
		top_level=`dirname ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}`
		if [ -h $top_level/default ]; then
			link_target=`readlink $top_level/default`
			[ `basename "$link_target"` = %{version} ] && rm -f $top_level/default
		fi
	fi
	rm -f /opt/modulefiles/pbs/%{version}
fi

%postun %{pbs_server}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	echo
	echo "NOTE: /etc/pbs.conf and the PBS_HOME directory must be deleted manually"
	echo
fi

%postun %{pbs_execution}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	echo
	echo "NOTE: /etc/pbs.conf and the PBS_HOME directory must be deleted manually"
	echo
fi

%postun %{pbs_client}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	echo
	echo "NOTE: /etc/pbs.conf must be deleted manually"
	echo
fi

%files %{pbs_server}
%defattr(-,root,root, -)
%dir %{pbs_prefix}
%{pbs_prefix}/*
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_rcp
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_iff
%{_sysconfdir}/profile.d/pbs.csh
%{_sysconfdir}/profile.d/pbs.sh
%if %{defined have_systemd}
%attr(644, root, root) %{_unitdir}/pbs.service
%else
%exclude %{_unitdir}/pbs.service
%endif
%exclude %{pbs_prefix}/unsupported/*.pyc
%exclude %{pbs_prefix}/unsupported/*.pyo

%files %{pbs_execution}
%defattr(-,root,root, -)
%dir %{pbs_prefix}
%{pbs_prefix}/*
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_rcp
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_iff
%{_sysconfdir}/profile.d/pbs.csh
%{_sysconfdir}/profile.d/pbs.sh
%if %{defined have_systemd}
%attr(644, root, root) %{_unitdir}/pbs.service
%else
%exclude %{_unitdir}/pbs.service
%endif
%exclude %{pbs_prefix}/bin/printjob_svr.bin
%exclude %{pbs_prefix}/etc/pbs_db_schema.sql
%exclude %{pbs_prefix}/etc/pbs_dedicated
%exclude %{pbs_prefix}/etc/pbs_holidays*
%exclude %{pbs_prefix}/etc/pbs_resource_group
%exclude %{pbs_prefix}/etc/pbs_sched_config
%exclude %{pbs_prefix}/lib*/init.d/sgiICEplacement.sh
%exclude %{pbs_prefix}/lib*/python/altair/pbs_hooks/*
%exclude %{pbs_prefix}/libexec/install_db
%exclude %{pbs_prefix}/sbin/pbs_comm
%exclude %{pbs_prefix}/sbin/pbs_dataservice
%exclude %{pbs_prefix}/sbin/pbs_ds_monitor
%exclude %{pbs_prefix}/sbin/pbs_ds_password
%exclude %{pbs_prefix}/sbin/pbs_ds_password.bin
%exclude %{pbs_prefix}/sbin/pbs_sched
%exclude %{pbs_prefix}/sbin/pbs_server
%exclude %{pbs_prefix}/sbin/pbs_server.bin
%exclude %{pbs_prefix}/sbin/pbsfs
%exclude %{pbs_prefix}/unsupported/*.pyc
%exclude %{pbs_prefix}/unsupported/*.pyo

%files %{pbs_client}
%defattr(-,root,root, -)
%dir %{pbs_prefix}
%{pbs_prefix}/*
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_iff
%{_sysconfdir}/profile.d/pbs.csh
%{_sysconfdir}/profile.d/pbs.sh
%exclude %{pbs_prefix}/bin/mpiexec
%exclude %{pbs_prefix}/bin/pbs_attach
%exclude %{pbs_prefix}/bin/pbs_tmrsh
%exclude %{pbs_prefix}/bin/printjob_svr.bin
%exclude %{pbs_prefix}/etc/pbs_db_schema.sql
%exclude %{pbs_prefix}/etc/pbs_dedicated
%exclude %{pbs_prefix}/etc/pbs_holidays*
%exclude %{pbs_prefix}/etc/pbs_resource_group
%exclude %{pbs_prefix}/etc/pbs_sched_config
%exclude %{pbs_prefix}/include
%exclude %{pbs_prefix}/lib*/MPI
%exclude %{pbs_prefix}/lib*/init.d
%exclude %{pbs_prefix}/lib*/python/altair/pbs_hooks
%exclude %{pbs_prefix}/lib*/python/pbs_bootcheck*
%exclude %{pbs_prefix}/libexec/install_db
%exclude %{pbs_prefix}/libexec/pbs_habitat
%exclude %{pbs_prefix}/libexec/pbs_init.d
%exclude %{pbs_prefix}/sbin/pbs_comm
%exclude %{pbs_prefix}/sbin/pbs_demux
%exclude %{pbs_prefix}/sbin/pbs_dataservice
%exclude %{pbs_prefix}/sbin/pbs_ds_monitor
%exclude %{pbs_prefix}/sbin/pbs_ds_password
%exclude %{pbs_prefix}/sbin/pbs_ds_password.bin
%exclude %{pbs_prefix}/sbin/pbs_idled
%exclude %{pbs_prefix}/sbin/pbs_mom
%exclude %{pbs_prefix}/sbin/pbs_rcp
%exclude %{pbs_prefix}/sbin/pbs_sched
%exclude %{pbs_prefix}/sbin/pbs_server
%exclude %{pbs_prefix}/sbin/pbs_server.bin
%exclude %{pbs_prefix}/sbin/pbs_upgrade_job
%exclude %{pbs_prefix}/sbin/pbsfs
%exclude %{pbs_prefix}/unsupported/*.pyc
%exclude %{pbs_prefix}/unsupported/*.pyo
%exclude %{_unitdir}/pbs.service


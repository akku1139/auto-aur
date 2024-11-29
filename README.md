# auto-aur

## Mirrors

- https://auto-aur.pages.dev/
- https://akku1139.github.io/auto-aur/
- https://auto-aur.netlify.app/
- https://auto-aur.vercel.app/
- https://auto-aur.web.app/
- https://auto-aur.firebaseapp.com/

https://www.hexabase.com/column/static-websites-for-frontend
https://www.staticwebsitehosting.org/

## Add packages

`packages.txt`

## Warning

- Do not edit `package.json`, `packages-manually.txt`, `non-aur/` and `public/` while building.
- Do not set a VCS package and the same normal package at the same time in `package.txt`.
- VCS packages must be installed after normal packages.

## TODOs

- Target Architecture (x86_64 v2, v3, v4, zen etc...)
- Package search
- Arch Linux 32 & Arch Linux ARM support
- sudo config
- git branch support
- Automatic failure handling

## Packages containing version change patch

```
inochi-creator
inochi-session
simplex-chat-git
```

## Memo

https://vendenic.link

```
# df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          73G   56G   18G  77% /
tmpfs            64M     0   64M   0% /dev
shm              64M     0   64M   0% /dev/shm
/dev/root        73G   56G   18G  77% /__w
tmpfs           3.2G  1.2M  3.2G   1% /run/docker.sock
```

```
[root@486a185e14c1 /]# mount
overlay on / type overlay (rw,relatime,lowerdir=/var/lib/docker/overlay2/l/X6IYKSD5J7PM2AP2R2XGPLKT5W:/var/lib/docker/overlay2/l/72CQZSMVD6GZ7WVEFRGHX2C5WD:/var/lib/docker/overlay2/l/7Q5HZRIAVX6PFSWLXSA5VCOX4C,upperdir=/var/lib/docker/overlay2/282dfa93d6c1996e4bcfcea8d41c018ce7e2c1af96afa5d02b22fcc2cff9df7e/diff,workdir=/var/lib/docker/overlay2/282dfa93d6c1996e4bcfcea8d41c018ce7e2c1af96afa5d02b22fcc2cff9df7e/work,nouserxattr)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev type tmpfs (rw,nosuid,size=65536k,mode=755,inode64)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=666)
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
cgroup on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot)
mqueue on /dev/mqueue type mqueue (rw,nosuid,nodev,noexec,relatime)
shm on /dev/shm type tmpfs (rw,nosuid,nodev,noexec,relatime,size=65536k,inode64)
/dev/sdb1 on /__t type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /__w type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /__e type ext4 (ro,relatime,discard,errors=remount-ro)
/dev/sdb1 on /__w/_actions type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /github/home type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /github/workflow type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /__w/_temp type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /etc/resolv.conf type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /etc/hostname type ext4 (rw,relatime,discard,errors=remount-ro)
/dev/sdb1 on /etc/hosts type ext4 (rw,relatime,discard,errors=remount-ro)
tmpfs on /run/docker.sock type tmpfs (rw,nosuid,nodev,size=3272920k,nr_inodes=819200,mode=755,inode64)
```

```
[root@486a185e14c1 /]# du -h --total -d1 /                                                                                                                                                                  [119/132]
3.1M    /tmp
14M     /var
4.0K    /home
4.0K    /boot
7.4M    /etc
8.0K    /root
84K     /run
12K     /srv
4.0K    /mnt
4.0K    /opt
458M    /usr
458M    /__e
8.8G    /__t
1.7M    /__w
36K     /github
0       /dev
0       /sys
du: cannot read directory '/proc/35/task/35/net': Invalid argument
du: cannot read directory '/proc/35/net': Invalid argument
du: cannot read directory '/proc/37/task/37/net': Invalid argument
du: cannot read directory '/proc/37/net': Invalid argument
du: cannot read directory '/proc/39/task/39/net': Invalid argument
du: cannot read directory '/proc/39/net': Invalid argument
du: cannot read directory '/proc/41/task/41/net': Invalid argument
du: cannot read directory '/proc/41/net': Invalid argument
du: cannot read directory '/proc/43/task/43/net': Invalid argument
du: cannot read directory '/proc/43/net': Invalid argument
du: cannot read directory '/proc/45/task/45/net': Invalid argument
du: cannot read directory '/proc/45/net': Invalid argument
du: cannot read directory '/proc/47/task/47/net': Invalid argument
du: cannot read directory '/proc/47/net': Invalid argument
du: cannot read directory '/proc/49/task/49/net': Invalid argument
du: cannot read directory '/proc/49/net': Invalid argument
du: cannot read directory '/proc/51/task/51/net': Invalid argument
du: cannot read directory '/proc/51/net': Invalid argument
du: cannot read directory '/proc/53/task/53/net': Invalid argument
du: cannot read directory '/proc/53/net': Invalid argument
du: cannot read directory '/proc/55/task/55/net': Invalid argument
du: cannot read directory '/proc/55/net': Invalid argument
du: cannot read directory '/proc/57/task/57/net': Invalid argument
du: cannot read directory '/proc/57/net': Invalid argument
du: cannot read directory '/proc/59/task/59/net': Invalid argument
du: cannot read directory '/proc/59/net': Invalid argument
du: cannot read directory '/proc/61/task/61/net': Invalid argument
du: cannot read directory '/proc/61/net': Invalid argument
du: cannot read directory '/proc/81/task/81/net': Invalid argument
du: cannot read directory '/proc/81/net': Invalid argument
du: cannot access '/proc/93/task/93/fd/4': No such file or directory
du: cannot access '/proc/93/task/93/fdinfo/4': No such file or directory
du: cannot access '/proc/93/fd/3': No such file or directory
du: cannot access '/proc/93/fdinfo/3': No such file or directory
0       /proc
9.7G    /
9.7G    total
```

```
[root@486a185e14c1 /]# du -h --total -d1 /__e
98M     /__e/node20_alpine
104M    /__e/node16
90M     /__e/node16_alpine
168M    /__e/node20
458M    /__e
458M    total
[root@486a185e14c1 /]# du -h --total -d1 /__t
128M    /__t/Ruby
5.2G    /__t/CodeQL
765M    /__t/go
621M    /__t/node
1.6G    /__t/Python
664M    /__t/PyPy
20K     /__t/Java_Temurin-Hotspot_jdk
8.8G    /__t
8.8G    total
[root@486a185e14c1 /]# du -h --total -d1 /__w
1.6M    /__w/_actions
16K     /__w/_PipelineMapping
8.0K    /__w/auto-aur
44K     /__w/_temp
1.7M    /__w
1.7M    total
[root@486a185e14c1 /]# rm -r /__t
rm: cannot remove '/__t': Device or resource busy
[root@486a185e14c1 /]# du -h --total -d1 /__t
4.0K    /__t
4.0K    total
```

```
[root@486a185e14c1 /]# du -h --total -d1 /                                                                                                                                                                   [12/132]
3.1M    /tmp
14M     /var
4.0K    /home
4.0K    /boot
7.4M    /etc
8.0K    /root
84K     /run
12K     /srv
4.0K    /mnt
4.0K    /opt
458M    /usr
458M    /__e
4.0K    /__t
1.7M    /__w
36K     /github
0       /dev
0       /sys
du: cannot read directory '/proc/35/task/35/net': Invalid argument
du: cannot read directory '/proc/35/net': Invalid argument
du: cannot read directory '/proc/37/task/37/net': Invalid argument
du: cannot read directory '/proc/37/net': Invalid argument
du: cannot read directory '/proc/39/task/39/net': Invalid argument
du: cannot read directory '/proc/39/net': Invalid argument
du: cannot read directory '/proc/41/task/41/net': Invalid argument
du: cannot read directory '/proc/41/net': Invalid argument
du: cannot read directory '/proc/43/task/43/net': Invalid argument
du: cannot read directory '/proc/43/net': Invalid argument
du: cannot read directory '/proc/45/task/45/net': Invalid argument
du: cannot read directory '/proc/45/net': Invalid argument
du: cannot read directory '/proc/47/task/47/net': Invalid argument
du: cannot read directory '/proc/47/net': Invalid argument
du: cannot read directory '/proc/49/task/49/net': Invalid argument
du: cannot read directory '/proc/49/net': Invalid argument
du: cannot read directory '/proc/51/task/51/net': Invalid argument
du: cannot read directory '/proc/51/net': Invalid argument
du: cannot read directory '/proc/53/task/53/net': Invalid argument
du: cannot read directory '/proc/53/net': Invalid argument
du: cannot read directory '/proc/55/task/55/net': Invalid argument
du: cannot read directory '/proc/55/net': Invalid argument
du: cannot read directory '/proc/57/task/57/net': Invalid argument
du: cannot read directory '/proc/57/net': Invalid argument
du: cannot read directory '/proc/59/task/59/net': Invalid argument
du: cannot read directory '/proc/59/net': Invalid argument
du: cannot read directory '/proc/61/task/61/net': Invalid argument
du: cannot read directory '/proc/61/net': Invalid argument
du: cannot read directory '/proc/81/task/81/net': Invalid argument
du: cannot read directory '/proc/81/net': Invalid argument
du: cannot access '/proc/100/task/100/fd/4': No such file or directory
du: cannot access '/proc/100/task/100/fdinfo/4': No such file or directory
du: cannot access '/proc/100/fd/3': No such file or directory
du: cannot access '/proc/100/fdinfo/3': No such file or directory
0       /proc
942M    /
942M    total
```

```
[root@6226c14edeeb auto-aur]# ls /dev
autofs           fb0    loop-control  mapper        ppp     sda    snapshot  tty12  tty20  tty29  tty37  tty45  tty53  tty61   ttyS11  ttyS2   ttyS28  ttyS8        vcs2   vcsa4  vcsu6
bsg              fd     loop0         mcelog        psaux   sda1   stderr    tty13  tty21  tty3   tty38  tty46  tty54  tty62   ttyS12  ttyS20  ttyS29  ttyS9        vcs3   vcsa5  vfio
btrfs-control    full   loop1         mem           ptmx    sdb    stdin     tty14  tty22  tty30  tty39  tty47  tty55  tty63   ttyS13  ttyS21  ttyS3   ttyprintk    vcs4   vcsa6  vga_arbiter
core             fuse   loop2         mqueue        ptp0    sdb1   stdout    tty15  tty23  tty31  tty4   tty48  tty56  tty7    ttyS14  ttyS22  ttyS30  udmabuf      vcs5   vcsu   vhost-net
cpu_dma_latency  hpet   loop3         net           pts     sdb14  tty       tty16  tty24  tty32  tty40  tty49  tty57  tty8    ttyS15  ttyS23  ttyS31  uinput       vcs6   vcsu1  vhost-vsock
cuse             hwrng  loop4         null          random  sdb15  tty0      tty17  tty25  tty33  tty41  tty5   tty58  tty9    ttyS16  ttyS24  ttyS4   urandom      vcsa   vcsu2  vmbus
dma_heap         input  loop5         nvme-fabrics  rfkill  sg0    tty1      tty18  tty26  tty34  tty42  tty50  tty59  ttyS0   ttyS17  ttyS25  ttyS5   userfaultfd  vcsa1  vcsu3  zero
dri              kmsg   loop6         nvram         root    sg1    tty10     tty19  tty27  tty35  tty43  tty51  tty6   ttyS1   ttyS18  ttyS26  ttyS6   vcs          vcsa2  vcsu4  zfs
ecryptfs         kvm    loop7         port          rtc0    shm    tty11     tty2   tty28  tty36  tty44  tty52  tty60  ttyS10  ttyS19  ttyS27  ttyS7   vcs1         vcsa3  vcsu5
```

```
[root@6226c14edeeb auto-aur]# lsblk
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop0     7:0    0   64M  1 loop
loop1     7:1    0   87M  1 loop
loop2     7:2    0 38.8M  1 loop
sda       8:0    0   75G  0 disk
└─sda1    8:1    0   75G  0 part
sdb       8:16   0   75G  0 disk
├─sdb1    8:17   0 74.9G  0 part /etc/hosts
│                                /etc/hostname
│                                /etc/resolv.conf
│                                /github/workflow
│                                /github/home
│                                /__w/_actions
│                                /__w/_temp
│                                /__t
│                                /__e
│                                /__w
├─sdb14   8:30   0    4M  0 part
└─sdb15   8:31   0  106M  0 part
```

```
[root@6226c14edeeb auto-aur]# mount /dev/root /mnt
[root@6226c14edeeb auto-aur]# ls /mnt
bin  boot  data  dev  etc  home  imagegeneration  lib  lib32  lib64  libx32  lost+found  media  mnt  opt  proc  root  run  sbin  snap  srv  sys  tmp  usr  var
```

```
[root@6bfed14bb3a6 auto-aur]# du -h --total -d1 /mnt
36K     /mnt/snap
92K     /mnt/tmp
5.2G    /mnt/var
16K     /mnt/data
12K     /mnt/dev
4.0K    /mnt/sys
2.2G    /mnt/home
4.0K    /mnt/proc
62M     /mnt/boot
655M    /mnt/etc
156M    /mnt/root
804K    /mnt/imagegeneration
8.0K    /mnt/run
4.0K    /mnt/srv
4.0K    /mnt/media
16K     /mnt/lost+found
4.0K    /mnt/mnt
12G     /mnt/opt
34G     /mnt/usr
53G     /mnt
53G     total
```

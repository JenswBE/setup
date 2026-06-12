# QEMU/KVM: Extend disk

1. Shutdown the VM
2. On the VM host: `sudo qemu-img resize /srv/libvirt/images/vm.qcow2 +50G`
3. Attach a GParted disk to the VM and update boot order to boot from the GParted disk
4. Start the VM
5. Use GParted to extend the existing partition to use the new space
6. Extend the LV using `sudo lvextend -l +100%FREE /dev/mapper/vg0-lv0` (Option `-r` to resize FS errors on `execpv`)
7. Extend the FS using `sudo resize2fs /dev/mapper/vg0-lv0`
8. Shutdown the VM and detach the GParted disk
9. Start the VM and verify the new disk space is available using `df -h`

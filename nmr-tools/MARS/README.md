# Running MARS 1.2 on a Modern System (Pop!_OS/Ubuntu)

**MARS 1.2** is a protein NMR assignment software from 2010. It relies on:
- Perl 5.10–5.14 (uses the deprecated `$[ = 1` array‑base feature).
- A 32‑bit compiled binary (`mars`) that requires 32‑bit system libraries.

On a modern 64‑bit Linux with Perl ≥5.16, you get the error:  
`Assigning non-zero to $[ is no longer possible`.  
Even with `perlbrew` installing older Perl, the 32‑bit binary may fail due to missing libraries.

The most reliable solution is to use **Docker with an old Ubuntu image** (12.04 Precise), which provides Perl 5.14 and allows installation of 32‑bit libraries without affecting your host.

---

## Steps that worked

### 1. Start a container with Ubuntu 12.04
```bash
docker run -it --rm \
  -v $(pwd):/work \
  -w /work \
  ubuntu:12.04 bash
```
- Mounts your current directory (containing the MARS tarball and input files) to `/work` inside the container.
- `--rm` removes the container after exit.

### 2. Extract MARS (if not already done)
```bash
tar -xzf mars-1.2_linux.tar.gz -C /opt
```
The binary will be at `/opt/mars-1.2_linux/bin/mars`.

### 3. Install 32‑bit libraries
The `mars` binary is 32‑bit and dynamically linked. Ubuntu 12.04 can run 32‑bit executables after installing the necessary libraries:
```bash
apt-get update
apt-get install -y libc6:i386 libstdc++6:i386
```
(If other libraries are missing, `ldd /opt/mars-1.2_linux/bin/mars` will show them; install similarly.)

### 4. Set the environment variable
```bash
export MARSHOME=/opt/mars-1.2_linux/bin
```

### 5. Run MARS on the example data
```bash
cd /work/mars-1.2_linux/examples/Input-1.2
/opt/mars-1.2_linux/bin/runmars mars.inp
```
You should see output like:
```
Use of assignment to $[ is deprecated ...   (harmless warning)
...
MARS has been successfully finished !!
```

---

### Save the configured container as an image
```bash
docker ps -a
docker commit <container-id> mars12-fixed
```
Then later run with:
```bash
docker run -it --rm -v /path/to/data:/data mars12-fixed \
  bash -c "export MARSHOME=/opt/mars-1.2_linux/bin && cd /data && /opt/mars-1.2_linux/bin/runmars mars.inp"
```



---

Now you can process your own data by placing input files in a mounted directory and running the same `runmars` command.

# WHITE01 — computer specification

Recorded: 2026-10-10
Source: hardware information supplied by the Director. This is a descriptive inventory, not a live hardware scan or benchmark.

## System

| Item | Specification |
| --- | --- |
| Computer name | WHITE01 |
| Operating system | Microsoft Windows 10 Pro |
| OS version | 10.0.19045, build 19045 |
| Architecture | x64-based PC |
| System manufacturer/model | ASUS / System Product Name |
| CPU | AMD Ryzen 5 5600X3D |
| CPU cores/threads | 6 cores / 12 logical processors |
| Reported CPU clock | 3301 MHz; snapshot, not a sustained-performance measurement |
| Motherboard | ASUS TUF GAMING B550-PLUS WIFI II, Rev X.0x |
| BIOS | American Megatrends Inc. 3002, dated 2023-02-23 |
| BIOS mode | UEFI |
| SMBIOS | 3.3 |
| Installed RAM | 32.0 GB |
| Reported usable physical RAM | 31.9 GB |
| GPU | AMD Radeon RX 6600 |
| GPU VRAM | 8 GB GDDR6, based on AMD product specification; not verified by a live scan |
| GPU driver version | 32.0.21045.5002 |
| Reported display | 2560 × 1440 at 60 Hz, 32-bit color |
| Time zone | Central Time, America/Chicago |

The supplied Windows Adapter RAM field reports 1,048,576 bytes. That value does not represent the RX 6600's actual dedicated memory; use the product specification pending Task Manager or another direct verification.

GPU specification source: [AMD Radeon RX 6600](https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6600.html).

## Storage volumes

Sizes and free space are the supplied snapshot. These are logical volumes; their physical disk mapping and interfaces have not been scanned. GB/TB labels retain the supplied Windows report values.

| Drive | Label | File system | Size | Free space | Medium / interface evidence |
| --- | --- | --- | --- | --- | --- |
| C: | Not supplied | NTFS | 439.44 GB | 315.21 GB | Unverified |
| D: | Dev | NTFS | 476.92 GB | 476.74 GB | Unverified |
| E: | Google Drive | FAT32 | 100.00 GB | 91.94 GB | Cloud-drive label; physical local backing unverified |
| F: | Games | exFAT | 3.64 TB | 1.63 TB | Unverified |
| G: | Games-SSD | NTFS | 931.01 GB | 816.08 GB | SSD indicated by label; Director believes SATA, not yet verified |
| H: | Storage | NTFS | 3.64 TB | 3.57 TB | Unverified |

All volumes were reported as uncompressed. Free-space values may change; do not treat them as current capacity checks before an installation.

## Memory snapshot

| Item | Reported value |
| --- | --- |
| Available physical memory | 14.3 GB |
| Total virtual memory | 36.6 GB |
| Available virtual memory | 7.41 GB |
| Page file space | 4.75 GB |
| Page file | C:\pagefile.sys |

Available memory reflects the programs running at the time of the supplied report. Virtual memory is not GPU VRAM and is not equivalent to physical RAM for inference performance.

## Firmware and virtualization snapshot

| Item | Reported state |
| --- | --- |
| Secure Boot | Off |
| Kernel DMA protection | Off |
| Virtualization-based security | Not enabled |
| Hyper-V VM monitor extensions | Yes |
| Hyper-V second-level address translation | Yes |
| Virtualization enabled in firmware | No |
| Hyper-V data execution protection | Yes |
| PCR7 configuration | Elevation required to view |
| Device encryption support | Elevation required to view |

These are recorded states, not instructions to alter firmware or security settings.

## Librarian context

Current project location supplied by the Director: `D:\Git\Librarian`.
Colab inputs: `colab\packs`.
Working review notes: `colab\notes`.
Review returns: `colab\returns`.

The local workflow currently uses model clients for Prime/worker and colab work. A client running on this PC does not establish that its model weights execute on this PC. No locally hosted inference engine, downloaded model, or measured inference speed was verified for this inventory.

## Proposed local inference experiment — not installed or benchmarked

A candidate starting point is llama.cpp's Windows Vulkan backend with a 7–8B instruction model in 4-bit GGUF. Suitability, GPU offload, context length and output quality must be measured on this machine. No throughput or model-fit guarantee is recorded.

Suggested first workload: a bounded Librarian page review with companion faces, returning proposed findings without changing a kernel seat.

AirLLM remains an experimental candidate. Its low-VRAM claims do not establish a supported or responsive Windows/RX 6600 configuration. The believed SATA storage interface is especially relevant to repeated weight streaming.

Runtime reference: [llama.cpp build documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md).

## Items to verify later

- Dedicated GPU memory in Task Manager or a direct GPU query.
- Physical drive models, disk-to-volume mapping, and SATA/NVMe interfaces.
- Available RAM and VRAM during a representative worker job.
- Actual prompt-processing and generation speed, context limits, and review accuracy.

User name, device identifiers and volume serial numbers are omitted because they are unnecessary for hardware planning.
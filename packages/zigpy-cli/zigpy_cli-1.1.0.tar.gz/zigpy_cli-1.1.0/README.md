# `zigpy-cli`

A unified command line interface for zigpy radios. The goal of this project is to allow
low-level network management from an intuitive command line interface and to group useful
Zigbee tools into a single binary.

## Installation

```console
$ pip install zigpy-cli
```

## Usage

```console
$ zigpy --help
Usage: zigpy [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  ota
  radio
  pcap
```

**Make sure ZHA, Zigbee2MQTT, deCONZ, etc. are disabled.** Any software controlling your
radio requires exclusive access to the hardware: if both are running at once, neither will work.

# Network commands
Network commands require the radio type to be specified. See `zigpy radio --help` for the list of supported types.
If your radio requires a different baudrate than the radio library default (mainly EZSP), you must specify it as a command line option. For example, `zigpy radio --baudrate 115200 ezsp backup -`.

## Network backup

```console
$ zigpy radio deconz /dev/ttyUSB0 backup deconz-backup.json
```

## Network restore

```console
$ zigpy radio znp /dev/ttyUSB1 restore deconz-backup.json
```

## Reading network information

```console
$ zigpy radio znp /dev/ttyUSB0 info
PAN ID:                0x718B
Extended PAN ID:       33:29:33:5e:30:42:64:48
Channel:               15
Channel mask:          [15]
NWK update ID:         0
Device IEEE:           00:12:4b:00:1c:ce:33:85
Device NWK:            0x0000
Network key:           cc:44:a6:4e:23:82:30:9e:35:0f:c6:6a:89:c8:dd:7d
Network key sequence:  0
```

## Forming a network

```console
$ zigpy -vvvv radio znp /dev/cu.usb* form
2021-07-12 13:24:54.764 host asyncio DEBUG Using selector: KqueueSelector
2021-07-12 13:24:54.933 host zigpy_znp.uart DEBUG Connecting to /dev/ttyUSB0 at 115200 baud
2021-07-12 13:24:54.940 host zigpy_znp.uart DEBUG Opened /dev/ttyUSB0 serial port
2021-07-12 13:24:54.941 host zigpy_znp.uart DEBUG Toggling RTS/CTS to skip CC2652R bootloader
2021-07-12 13:24:55.404 host zigpy_znp.uart DEBUG Connected to /dev/ttyUSB0 at 115200 baud
2021-07-12 13:24:55.404 host zigpy_znp.api DEBUG Waiting 1s before sending anything
2021-07-12 13:24:56.409 host zigpy_znp.api DEBUG Sending bootloader skip byte
...
PAN ID:                0xAA8A
Extended PAN ID:       35:8f:dc:b6:7a:19:33:c3
Channel:               15
Channel mask:          [15]
NWK update ID:         0
Device IEEE:           00:12:4b:00:1c:ce:33:85
Device NWK:            0x0000
Network key:           8c:2d:2d:a6:ca:95:30:04:11:6b:d5:dd:32:9e:b6:a8
Network key sequence:  0
2021-07-12 13:25:15.316 host zigpy_znp.uart DEBUG Closing serial port
```

## Performing an energy scan

```console
$ zigpy radio znp /dev/cu.usbserial-1420 energy-scan

Channel energy (mean of 1 / 5):
------------------------------------------------
 + Lower energy is better
 + Active Zigbee networks on a channel may still cause congestion
 + TX on 26 in North America may be with lower power due to regulations
 + Zigbee channels 15, 20, 25 fall between WiFi channels 1, 6, 11
 + Some Zigbee devices only join networks on channels 15, 20, and 25
------------------------------------------------
 - 11    80.00%  ################################################################################
 - 12    83.53%  ###################################################################################
 - 13    83.14%  ###################################################################################
 - 14    78.82%  ##############################################################################
 - 15    76.47%  ############################################################################
 - 16    72.16%  ########################################################################
 - 17    76.47%  ############################################################################
 - 18    75.69%  ###########################################################################
 - 19    72.16%  ########################################################################
 - 20    65.49%  #################################################################
 - 21    66.67%  ##################################################################
 - 22    70.59%  ######################################################################
 - 23    80.00%  ################################################################################
 - 24    64.31%  ################################################################
 - 25    77.25%  #############################################################################
 - 26*   81.96%  #################################################################################
```

## Reset a radio

```console
$ zigpy radio --baudrate 115200 ezsp /dev/serial/by-id/some-radio reset
```

## Permit joins

Mainly useful for testing requests.

```console
$ zigpy radio deconz /dev/ttyUSB0 permit -t 60
```

## Changing the network channel

Some devices (like older Aqara sensors) may not migrate.

```console
$ zigpy radio znp /dev/ttyUSB0 change-channel --channel 25
```

## Network scan

On supported radios, you can perform an active beacon scan for nearby 802.15.4 networks:

```console
$ zigpy radio ezsp /dev/ttyUSB0 network-scan --channels 11,15,20,25 --duration-exponent 3
channel: 11, network: 0x1D13 (00:07:81:00:0e:e9:d8:9f), permitting joins: 1, nwk update id: 0, lqi:  180, rssi: -66
channel: 11, network: 0x2857 (00:07:81:00:fc:9e:ef:95), permitting joins: 0, nwk update id: 0, lqi:  224, rssi: -55
channel: 11, network: 0x08C7 (00:07:81:00:50:d2:be:2e), permitting joins: 0, nwk update id: 0, lqi:  216, rssi: -57
channel: 15, network: 0x2ABB (00:07:81:00:c5:10:10:4b), permitting joins: 0, nwk update id: 0, lqi:  212, rssi: -58
Scanning channel 15
```

## Packet capture

On supported radios, you can capture packets and pipe the PCAP output to Wireshark:

```console
$ zigpy radio ezsp /dev/cu.SLAB_USBtoUART14 packet-capture -c 12,13,14,26 --interleave --channel-hop-period 1 -o - | wireshark -k -S -i -
```

If you have multiple adapters, you can capture with multiple interfaces concurrently:

```console
(
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART   packet-capture -c 11 --interleave -o -  &
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART8  packet-capture -c 15 --interleave -o -  &
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART10 packet-capture -c 20 --interleave -o -  &
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART13 packet-capture -c 25 --interleave -o -  &
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART14 packet-capture -c 12,13,14,26 --interleave --channel-hop-period 1 -o -  &
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART17 packet-capture -c 16,17,18,19 --interleave --channel-hop-period 1 -o -  &
    zigpy radio ezsp /dev/cu.SLAB_USBtoUART18 packet-capture -c 21,22,23,24 --interleave --channel-hop-period 1 -o -  &
    wait
) | zigpy pcap interleave-combine -o - | wireshark -k -S -i -
```

# OTA
## Display basic information about OTA files
```console
$ zigpy ota info 10047227-1.2-TRADFRI-cv-cct-unified-2.3.050.ota.ota.signed
Header: OTAImageHeader(upgrade_file_id=200208670, header_version=256, header_length=56, field_control=<FieldControl.0: 0>, manufacturer_id=4476, image_type=16902, file_version=587531825, stack_version=2, header_string='GBL GBL_tradfri_cv_cct_unified', image_size=208766, *device_specific_file=False, *hardware_versions_present=False, *key=ImageKey(manufacturer_id=4476, image_type=16902), *security_credential_version_present=False)
Number of subelements: 1
Validation result: ValidationResult.VALID
```

## Dump embedded firmware for further analysis

```console
$ zigpy ota dump-firmware 10047227-1.2-TRADFRI-cv-cct-unified-2.3.050.ota.ota.signed - \
      | commander ebl print /dev/stdin \
      | grep 'Ember Version'
Ember Version:    6.3.1.1
```

## Generate OTA index files

Create a JSON index for a given directory of firmwares:

```console
$ zigpy ota generate-index --ota-url-root="https://example.org/fw" path/to/firmwares/**/*.ota
2023-02-14 12:02:03.532 ubuntu zigpy_cli.ota INFO Parsing path/to/firmwares/fw/test.ota
2023-02-14 12:02:03.533 ubuntu zigpy_cli.ota INFO Writing path/to/firmwares/fw/test.ota
[
    {
        "binary_url": "https://example.org/fw/test.ota",
        "file_version": 1762356,
        "image_type": 1234,
        "manufacturer_id": 5678,
        "changelog": "",
        "checksum": "sha3-256:1ddaa649eb920dea9e5f002fe0d1443cc903ac0c1b26e7ad2c97b928edec2786"
    },
...
```

## Reconstruct an OTA image from a series of packet captures

Requires the `tshark` binary to be available.

```console
$ zigpy ota reconstruct-from-pcaps --add-network-key aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99 --output-root ./extracted/ *.pcap
Constructing image type=0x298b, version=0x00000005, manuf_code=0x115f: 157424 bytes
2023-02-22 03:39:51.406 ubuntu zigpy_cli.ota ERROR Missing 48 bytes starting at offset 0x0000ADA0: filling with 0xAB
2023-02-22 03:39:51.406 ubuntu zigpy_cli.ota ERROR Missing 48 bytes starting at offset 0x000106B0: filling with 0xAB
Constructing image type=0x298b, version=0x00000009, manuf_code=0x115f: 163136 bytes
```


# PCAP
## Re-calculate the FCS on a packet capture

Fixes a bug in current EmberZNet SDK releases:
```console
$ # Fix an existing capture
$ zigpy pcap fix-fcs input.pcap fixed.pcap
$ # Fix a capture from stdin and send it to stdout
$ bellows -d /dev/cu.GoControl_zigbee dump -w /dev/stdout | zigpy pcap fix-fcs - - | wireshark -k -S -i -
```

# Database
Attempt to recover a corrupted `zigbee.db` database:

```console
$ zigpy -v db recover broken.db fixed.db
2022-05-07 13:01:22.907 host zigpy_cli.database ERROR Failed to insert INSERT INTO "attributes_cache_v7"("_rowid_", "ieee", "endpoint_id", "cluster", "attrid", "value") VALUES( 14507477, '00:15:8d:00:02:5e:f9:ff', 1, 1027, 0, 1001.78 );: IntegrityError('UNIQUE constraint failed: attributes_cache_v7.ieee, attributes_cache_v7.endpoint_id, attributes_cache_v7.cluster, attributes_cache_v7.attrid')
2022-05-07 13:01:22.916 host zigpy_cli.database INFO Done
```

The final database will have no invalid constraints but data will likely be lost.
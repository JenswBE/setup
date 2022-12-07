# Loss of house and devices

## Assumptions

- House and devices are completely destroyed due to e.g. fire.

## Prerequisites

- Paper backup of OTP keys at another location, e.g. family house.
- Server with password vault is still live, e.g. VPS.

## Steps

1. Recover paper backup of OTP keys
2. Install [andOTP](https://github.com/andOTP/andOTP) or similar
3. Add OTP key of server with password vault
4. Download password vault
5. Recover data using Borg passphrase

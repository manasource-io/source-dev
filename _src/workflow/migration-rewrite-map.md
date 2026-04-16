# Migration rewrite map

This file records concrete legacy-to-canonical rewrites applied during Pass B.

- `habits/sunlight-exposure` → `habit/sunlight-exposure` (normalize)
- `habits/wake-time` → `circadian/wake-time` (rewrite)
- `info/fiber` → `orphans/info-fiber` (orphan)
- `mind/sleep-quality` → `restoration/sleep-quality` (rewrite)
- `activity/infrared-light` → `exercise/infrared-light` (rewrite)
- `activity/sauna` → `exercise/sauna` (rewrite)

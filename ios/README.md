# Gym Buddy iOS Companion

This folder contains a minimal SwiftUI scaffold for the Apple Health sync companion app.

## Responsibilities

- Request HealthKit read permissions
- Read daily steps, active energy, workouts, and exercise minutes
- Send read-only payloads to the FastAPI backend
- Keep the web app as the primary user experience

## Next Steps in Xcode

1. Create or open the Xcode project from this folder.
2. Enable the HealthKit capability.
3. Set your Apple developer team and bundle identifier.
4. Replace the demo API base URL in `HealthSyncService.swift`.
5. Test on a physical iPhone because HealthKit data is limited in Simulator.

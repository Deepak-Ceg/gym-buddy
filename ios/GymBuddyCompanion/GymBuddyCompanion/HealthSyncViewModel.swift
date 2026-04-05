import Foundation

final class HealthSyncViewModel: ObservableObject {
    @Published var statusMessage: String = "Ready to connect HealthKit."

    private let healthService = HealthKitService()
    private let syncService = HealthSyncService()

    func requestPermissions() {
        healthService.requestAuthorization { success, error in
            DispatchQueue.main.async {
                if let error {
                    self.statusMessage = "Permission failed: \(error.localizedDescription)"
                } else {
                    self.statusMessage = success ? "HealthKit access granted." : "HealthKit access was not granted."
                }
            }
        }
    }

    func syncToday() {
        healthService.fetchTodayMetrics { metrics in
            self.syncService.send(metrics: metrics) { result in
                DispatchQueue.main.async {
                    switch result {
                    case .success:
                        self.statusMessage = "Synced \(metrics.count) metrics to the backend."
                    case .failure(let error):
                        self.statusMessage = "Sync failed: \(error.localizedDescription)"
                    }
                }
            }
        }
    }
}

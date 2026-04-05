import Foundation
import HealthKit

final class HealthKitService {
    private let healthStore = HKHealthStore()

    func requestAuthorization(completion: @escaping (Bool, Error?) -> Void) {
        guard HKHealthStore.isHealthDataAvailable() else {
            completion(false, nil)
            return
        }

        let readTypes: Set = [
            HKObjectType.quantityType(forIdentifier: .stepCount)!,
            HKObjectType.quantityType(forIdentifier: .activeEnergyBurned)!,
            HKObjectType.quantityType(forIdentifier: .appleExerciseTime)!,
            HKObjectType.workoutType()
        ]

        healthStore.requestAuthorization(toShare: [], read: readTypes, completion: completion)
    }

    func fetchTodayMetrics(completion: @escaping ([[String: Any]]) -> Void) {
        let demoPayload: [[String: Any]] = [
            [
                "id": UUID().uuidString,
                "user_id": "user-1",
                "source": "apple_health",
                "date": "2026-04-05",
                "metric_type": "steps",
                "value": 9200,
                "unit": "count",
                "synced_at": ISO8601DateFormatter().string(from: Date())
            ]
        ]
        completion(demoPayload)
    }
}

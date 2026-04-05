import Foundation

final class HealthSyncService {
    private let session = URLSession.shared
    private let endpoint = URL(string: "http://localhost:8000/api/health-sync")!

    func send(metrics: [[String: Any]], completion: @escaping (Result<Void, Error>) -> Void) {
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let payload: [String: Any] = [
            "user_id": "user-1",
            "metrics": metrics
        ]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        } catch {
            completion(.failure(error))
            return
        }

        session.dataTask(with: request) { _, _, error in
            if let error {
                completion(.failure(error))
            } else {
                completion(.success(()))
            }
        }.resume()
    }
}

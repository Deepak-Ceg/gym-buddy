import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = HealthSyncViewModel()

    var body: some View {
        NavigationView {
            VStack(alignment: .leading, spacing: 16) {
                Text("Gym Buddy Sync")
                    .font(.largeTitle.bold())

                Text("Read steps and workouts from Apple Health, then sync them to the Gym Buddy backend.")
                    .foregroundColor(.secondary)

                Button("Request Health Access") {
                    viewModel.requestPermissions()
                }
                .buttonStyle(.borderedProminent)

                Button("Sync Today's Metrics") {
                    viewModel.syncToday()
                }
                .buttonStyle(.bordered)

                Text(viewModel.statusMessage)
                    .font(.footnote)
                    .foregroundColor(.secondary)

                Spacer()
            }
            .padding()
            .navigationTitle("Health Sync")
        }
    }
}

#Preview {
    ContentView()
}

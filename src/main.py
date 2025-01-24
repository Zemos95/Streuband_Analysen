import numpy as np
import matplotlib.pyplot as plt
from src import my_function, analyze_high_load_signal  # Importiere Funktion aus __init__.py


def main() -> None:
    # Simulationsparameter
    fs = 50  # Abtastfrequenz (50 Hz)
    t = np.linspace(0, 10, fs * 10)  # 10 Sekunden Daten

    # Unbelastetes Signal
    unloaded_signal = 2 * np.sin(2 * np.pi * 0.5 * t) + np.random.normal(0, 1, len(t))  # Rauschen mit Sinus

    # Belastetes Signal
    loaded_signal = 20 + 5 * np.sin(2 * np.pi * 0.5 * t) + np.random.normal(0, 3, len(t))

    # Gleitender Mittelwert
    window_size = 50  # Fenstergröße: 1 Sekunde
    def moving_average(signal, window_size):
        return np.convolve(signal, np.ones(window_size) / window_size, mode='same')

    moving_avg_unloaded = moving_average(unloaded_signal, window_size)
    moving_avg_loaded = moving_average(loaded_signal, window_size)

    # Toleranzband
    tolerance = 2  # ±2 µm/m
    upper_band_unloaded = moving_avg_unloaded + tolerance
    lower_band_unloaded = moving_avg_unloaded - tolerance
    upper_band_loaded = moving_avg_loaded + tolerance
    lower_band_loaded = moving_avg_loaded - tolerance

    # Markiere Punkte außerhalb des Toleranzbands
    def find_outliers_with_moving_band(signal, moving_avg, tolerance):
        upper_bound = moving_avg + tolerance
        lower_bound = moving_avg - tolerance
        outliers = (signal > upper_bound) | (signal < lower_bound)
        return outliers

    unloaded_outliers = find_outliers_with_moving_band(unloaded_signal, moving_avg_unloaded, tolerance)
    loaded_outliers = find_outliers_with_moving_band(loaded_signal, moving_avg_loaded, tolerance)

    # Abbildungen erstellen
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Plot 1: Unbelastetes Signal
    axes[0].plot(t, unloaded_signal, label="Unbelastetes Signal", alpha=0.7)
    axes[0].plot(t, moving_avg_unloaded, label="Gleitender Mittelwert", linewidth=2, color="blue")
    axes[0].plot(t, upper_band_unloaded, label="Obere Toleranzgrenze", linestyle="--", color="green")
    axes[0].plot(t, lower_band_unloaded, label="Untere Toleranzgrenze", linestyle="--", color="green")
    axes[0].scatter(t[unloaded_outliers], unloaded_signal[unloaded_outliers], color='red', label="Punkte außerhalb Toleranz", zorder=5)
    axes[0].set_title("Unbelastetes Signal mit gleitendem Mittelwert und Toleranzband")
    axes[0].set_xlabel("Zeit (s)")
    axes[0].set_ylabel("Dehnung (µm/m)")
    axes[0].legend()
    axes[0].grid()

    # Plot 2: Belastetes Signal
    axes[1].plot(t, loaded_signal, label="Belastetes Signal", alpha=0.7)
    axes[1].plot(t, moving_avg_loaded, label="Gleitender Mittelwert", linewidth=2, color="blue")
    axes[1].plot(t, upper_band_loaded, label="Obere Toleranzgrenze", linestyle="--", color="green")
    axes[1].plot(t, lower_band_loaded, label="Untere Toleranzgrenze", linestyle="--", color="green")
    axes[1].scatter(t[loaded_outliers], loaded_signal[loaded_outliers], color='red', label="Punkte außerhalb Toleranz", zorder=5)
    axes[1].set_title("Belastetes Signal mit gleitendem Mittelwert und Toleranzband")
    axes[1].set_xlabel("Zeit (s)")
    axes[1].set_ylabel("Dehnung (µm/m)")
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    analyze_high_load_signal()
    my_function()
    main()
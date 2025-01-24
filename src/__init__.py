import numpy as np
import matplotlib.pyplot as plt

def my_function() -> None:
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

    # Gleitende Standardabweichung berechnen
    def rolling_std(signal, window_size):
        std = np.array([
            np.std(signal[max(0, i - window_size // 2):min(len(signal), i + window_size // 2)]) 
            for i in range(len(signal))
        ])
        return std

    rolling_std_unloaded = rolling_std(unloaded_signal, window_size)
    rolling_std_loaded = rolling_std(loaded_signal, window_size)

    # ±1σ zum gleitenden Mittelwert hinzufügen
    upper_std_unloaded = moving_avg_unloaded + rolling_std_unloaded
    lower_std_unloaded = moving_avg_unloaded - rolling_std_unloaded
    upper_std_loaded = moving_avg_loaded + rolling_std_loaded
    lower_std_loaded = moving_avg_loaded - rolling_std_loaded

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
    axes[0].plot(t, upper_std_unloaded, label="Obere Grenze (±1σ)", linestyle=":", color="orange")
    axes[0].plot(t, lower_std_unloaded, label="Untere Grenze (±1σ)", linestyle=":", color="orange")
    axes[0].scatter(t[unloaded_outliers], unloaded_signal[unloaded_outliers], color='red', label="Punkte außerhalb Toleranz", zorder=5)
    axes[0].set_title("Unbelastetes Signal mit gleitendem Mittelwert, Toleranzband und ±1σ")
    axes[0].set_xlabel("Zeit (s)")
    axes[0].set_ylabel("Dehnung (µm/m)")
    axes[0].legend()
    axes[0].grid()

    # Plot 2: Belastetes Signal
    axes[1].plot(t, loaded_signal, label="Belastetes Signal", alpha=0.7)
    axes[1].plot(t, moving_avg_loaded, label="Gleitender Mittelwert", linewidth=2, color="blue")
    axes[1].plot(t, upper_band_loaded, label="Obere Toleranzgrenze", linestyle="--", color="green")
    axes[1].plot(t, lower_band_loaded, label="Untere Toleranzgrenze", linestyle="--", color="green")
    axes[1].plot(t, upper_std_loaded, label="Obere Grenze (±1σ)", linestyle=":", color="orange")
    axes[1].plot(t, lower_std_loaded, label="Untere Grenze (±1σ)", linestyle=":", color="orange")
    axes[1].scatter(t[loaded_outliers], loaded_signal[loaded_outliers], color='red', label="Punkte außerhalb Toleranz", zorder=5)
    axes[1].set_title("Belastetes Signal mit gleitendem Mittelwert, Toleranzband und ±1σ")
    axes[1].set_xlabel("Zeit (s)")
    axes[1].set_ylabel("Dehnung (µm/m)")
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    plt.show()


import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

def analyze_high_load_signal(fs=50, duration=1000, base_load=50, sin_amplitude=20, damping_factor=0.5, noise_amplitude=2, window_size=50, tolerance=2):
    """
    Analysiert ein Signal mit hoher Belastung (z. B. durch eine gedämpfte Überfahrt).

    Parameter:
        fs (int): Abtastfrequenz in Hz.
        duration (int): Dauer des Signals in Sekunden.
        base_load (float): Basiswert der Belastung in µm/m.
        sin_amplitude (float): Amplitude des sinusförmigen Belastungsanteils in µm/m.
        damping_factor (float): Dämpfungsfaktor für den Belastungsanteil.
        noise_amplitude (float): Amplitude des Streubands (Rauschen) in µm/m.
        window_size (int): Fenstergröße für den gleitenden Mittelwert.
        tolerance (float): Toleranzband in µm/m um den Mittelwert.

    Gibt:
        Einen Plot des Signals mit gleitendem Mittelwert, Toleranzband und ±1σ-Grenzen aus.
    """
    # Zeitvektor erstellen
    t = np.linspace(0, duration, fs * duration)

    # Belastungssignal: Gedämpfter Sinus
    damping = np.exp(-damping_factor * t)  # Dämpfungsfaktor
    load_signal = sin_amplitude * np.sin(2 * np.pi * 0.5 * t) * damping

    # Gesamtsignal: Basislast + Belastung + Rauschen
    high_load_signal = base_load + load_signal + noise_amplitude * np.random.normal(0, 1, len(t))

    # Gleitender Mittelwert
    def moving_average(signal, window_size):
        return np.convolve(signal, np.ones(window_size) / window_size, mode='same')

    moving_avg = moving_average(high_load_signal, window_size)

    # Gleitende Standardabweichung
    def rolling_std(signal, window_size):
        std = np.array([
            np.std(signal[max(0, i - window_size // 2):min(len(signal), i + window_size // 2)]) 
            for i in range(len(signal))
        ])
        return std

    rolling_std_signal = rolling_std(high_load_signal, window_size)

    # ±1σ-Grenzen
    upper_std = moving_avg + rolling_std_signal
    lower_std = moving_avg - rolling_std_signal

    # Toleranzband
    upper_band = moving_avg + tolerance
    lower_band = moving_avg - tolerance

    # Markiere Punkte außerhalb des Toleranzbands
    def find_outliers_with_moving_band(signal, moving_avg, tolerance):
        upper_bound = moving_avg + tolerance
        lower_bound = moving_avg - tolerance
        outliers = (signal > upper_bound) | (signal < lower_bound)
        return outliers

    outliers = find_outliers_with_moving_band(high_load_signal, moving_avg, tolerance)

    # Plot erstellen
    plt.figure(figsize=(14, 6))

    plt.plot(t, high_load_signal, label="Signal mit gedämpfter Belastung", alpha=0.7)
    plt.plot(t, moving_avg, label="Gleitender Mittelwert", linewidth=2, color="blue")
    plt.plot(t, upper_band, label="Obere Toleranzgrenze", linestyle="--", color="green")
    plt.plot(t, lower_band, label="Untere Toleranzgrenze", linestyle="--", color="green")
    plt.plot(t, upper_std, label="Obere Grenze (±1σ)", linestyle=":", color="orange")
    plt.plot(t, lower_std, label="Untere Grenze (±1σ)", linestyle=":", color="orange")
    plt.scatter(t[outliers], high_load_signal[outliers], color='red', label="Punkte außerhalb Toleranz", zorder=5)
    plt.title("Signal mit gedämpfter Belastung und Analyse der Grenzen")
    plt.xlabel("Zeit (s)")
    plt.ylabel("Dehnung (µm/m)")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


import numpy as np
import pandas as pd
import os

def generate_cycle_productivity_dataset(n_samples=3000, random_state=42):
    """
    Generates an extended dataset modeling cycle-based women's productivity,
    including Period Tracking, Delayed Periods, and PCOD/PCOS health conditions.
    """
    np.random.seed(random_state)
    
    # 1. Cycle Phases
    phases = ['Menstrual', 'Follicular', 'Ovulation', 'Luteal']
    cycle_phase = np.random.choice(phases, size=n_samples, p=[0.25, 0.25, 0.20, 0.30])
    
    # 2. Demographic & Work Environment
    age = np.random.randint(18, 51, size=n_samples)
    work_modes = ['Remote', 'Hybrid', 'In-Office']
    work_mode = np.random.choice(work_modes, size=n_samples, p=[0.4, 0.35, 0.25])
    
    # 3. Health Conditions: PCOD / PCOS prevalence (~18%)
    pcod_flag = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.18, 0.82])
    
    # 4. Period Tracking & Irregularity Metrics
    cycle_length_days = np.zeros(n_samples, dtype=int)
    period_delay_days = np.zeros(n_samples, dtype=int)
    hormonal_imbalance_score = np.zeros(n_samples, dtype=int)
    symptom_severity = np.zeros(n_samples, dtype=int)
    
    sleep_hours = np.zeros(n_samples)
    stress_level = np.zeros(n_samples, dtype=int)
    pain_level = np.zeros(n_samples, dtype=int)
    mood_score = np.zeros(n_samples, dtype=int)
    energy_level = np.zeros(n_samples, dtype=int)
    
    for i in range(n_samples):
        phase = cycle_phase[i]
        has_pcod = (pcod_flag[i] == 'Yes')
        
        # PCOD / PCOS impact on cycle length & delay
        if has_pcod:
            c_len = np.random.normal(42, 8)       # Irregular longer cycles (30-60 days)
            delay = np.random.normal(12, 6)       # Significant period delays (5-28 days)
            h_score = np.random.normal(7.5, 1.4)  # High hormonal imbalance
            s_sev = np.random.normal(7.2, 1.5)    # High symptom severity (acne, bloating, weight changes)
        else:
            c_len = np.random.normal(28, 2.5)     # Normal cycle (24-32 days)
            delay = np.random.normal(1.2, 1.5)    # Minimal/no delay (0-4 days)
            h_score = np.random.normal(3.2, 1.5)  # Low/normal hormonal imbalance
            s_sev = np.random.normal(3.5, 1.6)    # Moderate/low general symptoms
            
        cycle_length_days[i] = int(np.clip(round(c_len), 21, 65))
        period_delay_days[i] = int(np.clip(round(delay), 0, 35))
        hormonal_imbalance_score[i] = int(np.clip(round(h_score), 1, 10))
        symptom_severity[i] = int(np.clip(round(s_sev), 1, 10))
        
        # Phase dependent baseline with PCOD compounding factors
        pcod_pain_boost = 1.8 if has_pcod else 0.0
        pcod_stress_boost = 1.5 if has_pcod else 0.0
        pcod_energy_drop = 1.4 if has_pcod else 0.0
        
        if phase == 'Menstrual':
            sleep = np.random.normal(7.2, 1.2)
            stress = np.random.normal(6.5 + pcod_stress_boost, 1.8)
            pain = np.random.normal(6.8 + pcod_pain_boost, 1.9)
            mood = np.random.normal(4.8 - (pcod_stress_boost * 0.5), 1.6)
            energy = np.random.normal(4.2 - pcod_energy_drop, 1.5)
        elif phase == 'Follicular':
            sleep = np.random.normal(7.6, 0.9)
            stress = np.random.normal(4.2 + (pcod_stress_boost * 0.5), 1.5)
            pain = np.random.normal(2.1 + (pcod_pain_boost * 0.4), 1.2)
            mood = np.random.normal(7.4, 1.3)
            energy = np.random.normal(7.6 - (pcod_energy_drop * 0.5), 1.4)
        elif phase == 'Ovulation':
            sleep = np.random.normal(7.8, 0.8)
            stress = np.random.normal(3.8 + (pcod_stress_boost * 0.4), 1.4)
            pain = np.random.normal(1.8 + (pcod_pain_boost * 0.3), 1.0)
            mood = np.random.normal(8.5, 1.1)
            energy = np.random.normal(8.8 - (pcod_energy_drop * 0.4), 1.2)
        else:  # Luteal
            sleep = np.random.normal(7.0, 1.1)
            stress = np.random.normal(5.8 + pcod_stress_boost, 1.7)
            pain = np.random.normal(3.8 + pcod_pain_boost, 1.5)
            mood = np.random.normal(5.6 - (pcod_stress_boost * 0.4), 1.6)
            energy = np.random.normal(5.5 - pcod_energy_drop, 1.6)
            
        sleep_hours[i] = round(float(np.clip(sleep, 4.0, 10.5)), 1)
        stress_level[i] = int(np.clip(round(stress), 1, 10))
        pain_level[i] = int(np.clip(round(pain), 1, 10))
        mood_score[i] = int(np.clip(round(mood), 1, 10))
        energy_level[i] = int(np.clip(round(energy), 1, 10))

    # 5. Target Variable: Productivity Score (0 - 100)
    phase_offsets = {'Menstrual': -4.5, 'Follicular': +3.5, 'Ovulation': +6.0, 'Luteal': -2.0}
    phase_effect = np.array([phase_offsets[p] for p in cycle_phase])
    pcod_penalty = np.where(pcod_flag == 'Yes', -3.8, 0.0)
    delay_penalty = -0.18 * period_delay_days
    
    raw_productivity = (
        12.0 
        + 4.00 * energy_level 
        + 3.75 * sleep_hours 
        + 2.50 * mood_score 
        - 2.35 * stress_level 
        - 2.00 * pain_level 
        + phase_effect
        + pcod_penalty
        + delay_penalty
        + np.random.normal(0, 3.2, size=n_samples)
    )
    
    productivity_score = np.clip(np.round(raw_productivity, 1), 10.0, 100.0)
    
    df = pd.DataFrame({
        'User_ID': [f'USR_{1000 + i}' for i in range(n_samples)],
        'Age': age,
        'Cycle_Phase': cycle_phase,
        'PCOS_PCOD_Condition': pcod_flag,
        'Cycle_Length_Days': cycle_length_days,
        'Period_Delay_Days': period_delay_days,
        'Hormonal_Imbalance_Score': hormonal_imbalance_score,
        'Symptom_Severity': symptom_severity,
        'Sleep_Hours': sleep_hours,
        'Stress_Level': stress_level,
        'Pain_Level': pain_level,
        'Mood_Score': mood_score,
        'Energy_Level': energy_level,
        'Work_Mode': work_mode,
        'Productivity_Score': productivity_score
    })
    
    # Controlled missing values & duplicates
    missing_sleep = np.random.choice(n_samples, size=int(n_samples * 0.015), replace=False)
    missing_stress = np.random.choice(n_samples, size=int(n_samples * 0.015), replace=False)
    df.loc[missing_sleep, 'Sleep_Hours'] = np.nan
    df.loc[missing_stress, 'Stress_Level'] = np.nan
    
    duplicates = df.iloc[:10].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    return df

if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'womens_cycle_productivity_dataset.csv')
    
    df = generate_cycle_productivity_dataset(n_samples=3000)
    df.to_csv(csv_path, index=False)
    print(f"[SUCCESS] Extended PCOD & Cycle Tracking Dataset created at: {csv_path}")
    print(f"Dataset shape: {df.shape}")
    print(df.head())

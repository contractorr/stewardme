# Electrical and Electronics Engineering

## Overview

Electrical engineering harnesses electromagnetic phenomena to generate, transmit, and utilize electrical power while electronics manipulates electrons in semiconductors to process information, communicate, and control systems. Together, they enabled the electrical age (power grids, motors), the information age (computers, internet), and continue driving automation, renewable energy, and artificial intelligence. Modern civilization runs on electricity—this chapter explores how it's generated, distributed, and applied.

## Fundamentals of Electricity

### Charge, Current, and Voltage

**Electric charge (Q)**: Fundamental property; measured in Coulombs (C)
- Electron: -1.602 × 10⁻¹⁹ C
- Proton: +1.602 × 10⁻¹⁹ C
- **Current is flow of charge**

**Current (I)**: Rate of charge flow; I = dQ/dt
- Unit: Ampere (A) = 1 C/s
- **1 amp = 6.24 × 10¹⁸ electrons/second**
- **Conventional current**: Positive charge flow direction (opposite of electron flow)

**Voltage (V)**: Electrical potential difference; energy per unit charge
- Unit: Volt (V) = Joule/Coulomb
- **Analogy**: Water pressure in pipe
- Creates electric field driving current

**Resistance (R)**: Opposition to current flow
- Unit: Ohm (Ω)
- **Analogy**: Pipe friction

**Ohm's Law**: V = IR
- Fundamental relationship
- Linear for resistors (constant R)

**Power**: P = VI = I²R = V²/R
- Rate of energy transfer
- Unit: Watt (W) = J/s

**Example**: 100W lightbulb at 120V
- I = P/V = 100/120 = 0.83 A
- R = V/I = 120/0.83 = 144 Ω

### Circuit Elements

**Resistor**: Dissipates energy as heat
- **Series**: R_total = R₁ + R₂ + ...
- **Parallel**: 1/R_total = 1/R₁ + 1/R₂ + ...

**Capacitor**: Stores energy in electric field
- Q = CV where C = capacitance (Farads)
- **Current-voltage**: I = C(dV/dt)
- **Blocks DC, passes AC** (charging/discharging)
- Applications: Filtering, timing, energy storage

**Inductor**: Stores energy in magnetic field
- V = L(dI/dt) where L = inductance (Henrys)
- **Opposes current changes**
- Applications: Filters, transformers, motors

### AC vs. DC

**Direct Current (DC)**: Constant voltage/current over time
- Batteries, solar panels, electronics
- Easier to store (batteries)
- Early power systems (Edison)

**Alternating Current (AC)**: Sinusoidal, periodically reversing
- V(t) = V_peak sin(2πft)
- Frequency: f = 60 Hz (US), 50 Hz (Europe)
- **Modern power grids** use AC

**AC advantages**:
- **Transformers**: Easy voltage conversion (step up for transmission, step down for use)
- Lower transmission losses (high voltage → low current → I²R losses reduced)
- Simpler generators
- Won "War of Currents" (Tesla/Westinghouse vs. Edison)

**RMS voltage**: V_rms = V_peak/√2
- "Effective" voltage (equivalent DC for power)
- US household: 120V RMS ≈ 170V peak

## Power Systems

### Power Generation

**Synchronous generator** (alternator): Rotating magnetic field induces AC voltage in stationary coils

**Key components**:
1. **Rotor**: Electromagnet (supplied DC) or permanent magnet
2. **Stator**: Stationary coils where voltage induced
3. **Prime mover**: Turbine (steam, gas, hydro, wind) rotates rotor

**Synchronous speed**: n = 120f/p (RPM)
- f: Frequency (60 Hz)
- p: Number of poles
- **60 Hz generator with 2 poles → 3600 RPM**

**Three-phase power**: Three AC voltages 120° apart
- More efficient transmission (less copper)
- Constant instantaneous power (single-phase pulsates)
- Simpler motors (self-starting, smoother torque)
- **Standard for power generation and transmission**

### Power Transmission

**High-voltage transmission**: Reduces I²R losses

**Example**: Transmit 1000 MW over 300 miles
- At 10 kV: I = 100,000 A → massive losses
- At 500 kV: I = 2,000 A → 2500× lower losses

**Transmission voltages**:
- Local transmission: 69-138 kV
- Regional: 230-345 kV
- Long-distance: 500-765 kV

**Transformer**: Voltage conversion via electromagnetic induction
- V₂/V₁ = N₂/N₁ (turns ratio)
- No moving parts, 98-99% efficient
- **Key enabler** of AC power systems

**Power grid structure**:
1. **Generation**: Power plants (10-25 kV output)
2. **Step-up transformer**: Increase to transmission voltage
3. **Transmission lines**: High voltage, long distance
4. **Substations**: Step down to distribution voltage (13-35 kV)
5. **Distribution lines**: Local delivery
6. **Distribution transformers**: Step down to utilization (120/240V residential, 480V industrial)

**Grid stability**:
- **Frequency must stay constant** (60.00 Hz ± 0.05 Hz)
- Generation must exactly match load every instant
- Spinning reserve: Extra capacity to handle fluctuations
- Load shedding: Drop customers if insufficient generation (blackout prevention)

### Smart Grid

**Traditional grid**: One-way power flow, limited monitoring

**Smart grid**: Two-way communication, distributed generation, automation

**Features**:
- **Advanced metering** (AMI): Real-time usage data
- **Distributed generation**: Solar panels, wind turbines feed back to grid
- **Demand response**: Adjust load based on availability (e.g., defer EV charging)
- **Self-healing**: Automatically reroute around faults
- **Energy storage**: Batteries smooth renewable intermittency

**Challenges**:
- **Intermittent renewables**: Solar/wind variable; need storage or backup
- **Cybersecurity**: Grid increasingly network-connected
- **Bidirectional power flow**: Designed for one-way; requires new protection schemes

## Electronics: Semiconductors and Circuits

### Semiconductors

**Conductor**: Low resistance (metals—free electrons)

**Insulator**: High resistance (glass, rubber—no free charge carriers)

**Semiconductor**: Conductivity between; controlled by doping
- Pure silicon: Poor conductor
- **Doped**: Add impurities to control conductivity

**N-type**: Extra electrons (negative charge carriers)
- Doped with phosphorus, arsenic (group 15)

**P-type**: "Holes" (absence of electrons, act as positive charge carriers)
- Doped with boron, gallium (group 13)

### PN Junction Diode

**Structure**: P-type and N-type semiconductor joined

**Behavior**:
- **Forward bias** (positive to P, negative to N): Conducts (low resistance)
- **Reverse bias**: Blocks current (high resistance)
- **One-way valve** for current

**Applications**:
- **Rectifier**: Convert AC to DC
- **LED**: Light-emitting diode (emits photons when conducting)
- **Solar cell**: Reverse operation (photons create current)
- **Zener diode**: Voltage regulation (controlled breakdown)

### Transistor

**Invention** (1947, Bell Labs): Revolutionized electronics
- Replaced vacuum tubes (large, hot, fragile, power-hungry)

**Bipolar Junction Transistor (BJT)**:
- Three layers: NPN or PNP
- **Small base current controls large collector current**
- **Amplifier** or **switch**

**Field-Effect Transistor (FET)**, especially **MOSFET**:
- Voltage on gate controls current from drain to source
- **No gate current** (very high input impedance)
- **Dominant in digital circuits** (computers, microprocessors)

**Transistor as switch**: Foundation of digital logic
- **Binary**: ON (1) or OFF (0)
- **Logic gates**: AND, OR, NOT, NAND, NOR, XOR
- **Computers**: Billions of transistor switches

### Integrated Circuits (ICs)

**Invention** (1958-59, Kilby/Noyce): Multiple components on single silicon chip

**Scale evolution**:
- **SSI** (1960s): 10-100 transistors
- **MSI** (1970s): 100-1,000 transistors
- **LSI** (1970s): 1,000-100,000
- **VLSI** (1980s+): 100,000+
- **Modern CPUs** (2020s): 50+ billion transistors

**Moore's Law** (1965): Transistor count doubles every ~2 years
- Held for 50+ years
- Driven by photolithography advances (smaller features)
- **Transistor size**: 5nm in 2020s (few dozen atoms across!)
- Approaching physical limits (quantum tunneling, heat dissipation)

**Fabrication** (semiconductor fab):
1. Silicon wafer (300 mm diameter)
2. Photolithography: Pattern circuits using light (193 nm UV, extreme UV)
3. Doping: Ion implantation
4. Deposition: Add layers (metal, insulator)
5. Etching: Remove material
6. Repeat 30-50 layers
7. Test and package

**Cost**: Modern fab ~$10-20 billion
- Only a few companies can afford (Intel, TSMC, Samsung)
- Economies of scale critical

### Digital Logic and Microprocessors

**Logic gates**: Implement Boolean functions

**Example - Full Adder**:
- Adds three 1-bit numbers (A, B, carry-in)
- Outputs: Sum, carry-out
- Built from XOR, AND, OR gates
- **Chain together** for multi-bit addition

**CPU (Central Processing Unit)**:
- **ALU** (Arithmetic Logic Unit): Performs calculations
- **Control Unit**: Fetches instructions, decodes, coordinates
- **Registers**: Fast memory inside CPU
- **Cache**: Intermediate-speed memory

**Clock speed**: Operations per second
- Modern CPUs: 3-5 GHz (billions of cycles/second)
- Higher isn't always better (power, heat, diminishing returns)

**Performance factors**:
- Clock speed
- Instructions per cycle (IPC)
- Number of cores (parallel processing)
- Cache size and speed
- Architecture efficiency

**GPU** (Graphics Processing Unit): Specialized for parallel operations
- Thousands of simple cores (vs. few complex CPU cores)
- Excellent for graphics, machine learning (matrix operations)

## Analog Electronics

### Amplifiers

**Purpose**: Increase signal amplitude (voltage, current, or power)

**Operational Amplifier (Op-Amp)**:
- Very high gain (100,000+)
- Very high input impedance, low output impedance
- **Ideal op-amp assumptions** simplify circuit analysis
- **Configurations**: Inverting, non-inverting, difference, summing, integrator, differentiator

**Applications**:
- Audio amplification (speakers, microphones)
- Sensors (amplify weak signals)
- Filters (active filters using op-amps)
- Analog computation (solve differential equations)

### Filters

**Purpose**: Allow certain frequencies, block others

**Types**:
- **Low-pass**: Pass low frequencies, block high (smoothing, anti-aliasing)
- **High-pass**: Pass high frequencies, block low (AC coupling, noise removal)
- **Band-pass**: Pass frequencies in range (radio tuning, audio equalizers)
- **Band-stop**: Block frequencies in range (notch filter, 60 Hz noise removal)

**Passive filters**: Resistors, capacitors, inductors only
- Simple, no power required
- Limited performance

**Active filters**: Include amplifiers (op-amps)
- Better performance (sharper cutoffs, gain)
- Require power supply

### Signal Processing

**Analog-to-Digital Conversion (ADC)**: Converts continuous voltage to digital number
- **Sampling**: Measure at discrete time intervals
- **Quantization**: Round to nearest digital level
- **Sampling theorem** (Nyquist): Must sample at >2× highest frequency to avoid aliasing

**Digital-to-Analog Conversion (DAC)**: Converts digital number to voltage
- Audio output, motor control, video signals

**Digital Signal Processing (DSP)**:
- Process signals as digital data
- Advantages: Precision, flexibility, repeatability, no drift
- Applications: Audio processing, image processing, communications, control systems

## Communication Systems

### Modulation

**Problem**: Information signals (voice, data) are low frequency; antennas and propagation require high frequency

**Solution**: Modulate (encode) information onto high-frequency carrier wave

**Amplitude Modulation (AM)**: Vary carrier amplitude
- Simple, robust
- Susceptible to noise
- AM radio (535-1605 kHz)

**Frequency Modulation (FM)**: Vary carrier frequency
- Better noise immunity
- Requires more bandwidth
- FM radio (88-108 MHz)

**Phase Modulation (PM)**: Vary carrier phase
- Used in digital communications

**Digital modulation** (for data):
- **ASK** (Amplitude Shift Keying): Different amplitudes = different bits
- **FSK** (Frequency Shift Keying): Different frequencies
- **PSK** (Phase Shift Keying): Different phases
- **QAM** (Quadrature Amplitude Modulation): Combined amplitude and phase; high data rates (WiFi, LTE)

### Wireless Communication

**Electromagnetic waves**: Electric and magnetic fields propagating through space at speed of light

**Frequency spectrum**:

| Band | Frequency | Wavelength | Applications |
|------|-----------|----------|---------------|
| **ELF** | 3-30 Hz | 10,000-100,000 km | Submarine communication |
| **VLF** | 3-30 kHz | 10-100 km | Navigation |
| **LF/MF** | 30-3000 kHz | 100 m - 10 km | AM radio |
| **HF** | 3-30 MHz | 10-100 m | Shortwave, amateur radio |
| **VHF** | 30-300 MHz | 1-10 m | FM radio, TV |
| **UHF** | 300-3000 MHz | 10 cm - 1 m | TV, cellular, GPS |
| **Microwave** | 3-300 GHz | 1 mm - 10 cm | WiFi, radar, satellite |
| **Infrared** | 300 GHz - 400 THz | 780 nm - 1 mm | Fiber optics, remote controls |

**Antenna**: Converts electrical signal ↔ electromagnetic waves
- Length related to wavelength (typically λ/2 or λ/4)
- Lower frequency → larger antenna (AM tower hundreds of feet; cell phone antenna inches)

**Propagation**:
- **Line-of-sight**: High frequencies (FM, cell, WiFi)
- **Ground wave**: Medium frequencies follow Earth's curvature (AM radio)
- **Sky wave**: HF reflects off ionosphere (long-distance shortwave)

**Cellular networks**:
- Divide area into cells
- Each cell has base station
- **Frequency reuse**: Non-adjacent cells use same frequencies
- **Handoff**: Switch base stations as mobile moves
- **Generations**: 1G (analog), 2G (digital voice), 3G (mobile data), 4G/LTE (high-speed data), 5G (ultra-high speed, low latency)

### Fiber Optics

**Principle**: Total internal reflection confines light in fiber core

**Advantages over copper**:
- **Enormous bandwidth**: Terabits/second
- **Low loss**: Signals travel 100+ km without amplification
- **Immune to electromagnetic interference**
- **Small and light**

**Structure**:
- **Core**: Carries light (glass, 8-50 μm diameter)
- **Cladding**: Lower refractive index, reflects light back to core
- **Coating**: Protective layer

**Applications**:
- **Long-haul communications**: Undersea cables (transatlantic, transpacific)
- **Internet backbone**: Connecting cities, data centers
- **Fiber-to-the-home**: Gigabit residential internet

## Control Systems

### Feedback Control

**Open-loop control**: No feedback (e.g., toaster timer)
- Simple but inaccurate (disturbances not corrected)

**Closed-loop control**: Measures output, adjusts input to achieve desired output

**Components**:
1. **Reference** (setpoint): Desired value
2. **Sensor**: Measures actual output
3. **Controller**: Compares actual to desired, determines action
4. **Actuator**: Implements action
5. **Plant**: System being controlled

**Example - Cruise control**:
- Setpoint: Desired speed (70 mph)
- Sensor: Speedometer
- Controller: Cruise control module
- Actuator: Throttle
- Plant: Vehicle dynamics

**PID Controller** (Proportional-Integral-Derivative):
- **P** (Proportional): Error × K_p
  - Fast response
  - Can leave steady-state error
- **I** (Integral): ∫Error × K_i
  - Eliminates steady-state error
  - Can cause overshoot
- **D** (Derivative): (dError/dt) × K_d
  - Reduces overshoot and oscillation
  - Sensitive to noise

**Tuning**: Adjust K_p, K_i, K_d for desired response
- Fast response vs. stability
- No overshoot vs. quick settling

**Applications**: Temperature control, motor speed control, process control, autopilots

### Automation and Robotics

**Programmable Logic Controller (PLC)**: Industrial computer for automation
- Rugged, reliable
- Programmed with ladder logic (graphical)
- Controls manufacturing, water treatment, power plants

**Industrial robot**: Programmable manipulator
- **Articulated arm**: Multiple rotating joints (most common)
- **SCARA**: Selective Compliance Articulated Robot Arm (assembly)
- **Delta**: Parallel linkage (high-speed pick-and-place)

**Sensors**: Provide feedback
- Position (encoders, potentiometers)
- Force/torque
- Vision (cameras with image processing)
- Proximity, touch

**Applications**:
- **Manufacturing**: Welding, painting, assembly
- **Warehouse**: Automated guided vehicles (AGVs), sorting
- **Agriculture**: Autonomous tractors, harvesters
- **Autonomous vehicles**: Self-driving cars

## Real-World Case Studies

### Smart Phone

**Integration of electronics disciplines**:

**Power**: Battery (3.7V Li-ion, 10-15 Wh)
- Power management IC (buck/boost converters, charging)

**Processing**:
- Application processor (CPU, GPU, neural engine)
  - 5nm technology, 15B+ transistors
  - 2-3 GHz, 6-8 cores
- Modem (cellular communication)

**Memory**:
- RAM: 4-12 GB (DRAM)
- Storage: 64-1024 GB (Flash, NAND)

**Sensors**:
- Accelerometer, gyroscope (motion)
- Magnetometer (compass)
- Proximity, ambient light
- Barometer (altitude)
- GPS
- Cameras (2-4, 12+ MP)

**Communication**:
- Cellular (4G/5G)
- WiFi (2.4/5 GHz)
- Bluetooth
- NFC (contactless payments)
- GPS/GNSS

**Display**: OLED or LCD, 1080p-4K resolution
- Touchscreen (capacitive)

**Power consumption challenge**: All these systems in ~15 Wh battery, last full day
- Aggressive power management
- Low-power modes
- Efficient processors

### Electric Vehicle

**Battery pack**: 50-100 kWh (Tesla Model 3: 75 kWh)
- 4,000-7,000 lithium-ion cells
- 400V nominal (some moving to 800V)
- Battery Management System (BMS): Monitors cells, balances charge, thermal management

**Inverter**: Converts DC (battery) to AC (motor)
- High power (200-300 kW)
- High efficiency (>95%)
- SiC (silicon carbide) transistors: Higher efficiency, smaller size than Si

**Motor**: 3-phase AC induction or permanent magnet synchronous
- 200-500 HP
- Very high efficiency (85-95% over wide range)
- Integrated gearbox (typically single-speed, 9:1 reduction)

**Charging**:
- **Level 1**: 120V, 12A → 1.4 kW (3-5 miles/hour)
- **Level 2**: 240V, 40A → 10 kW (25 miles/hour)
- **DC Fast Charge**: 50-350 kW (150-1000 miles/hour)

**Power electronics complexity**:
- DC-DC converters (400V → 12V for accessories)
- Onboard charger (AC → DC)
- Regenerative braking (motor as generator, charge battery)

**Range anxiety solution**: Larger batteries, faster charging, more efficient systems

### Data Center

**Power requirements**: 10-100 MW (medium-large facility)
- Equivalent to small city
- **Power Usage Effectiveness (PUE)**: Total power / IT power
  - Ideal: 1.0 (all power to computing)
  - Good: 1.2-1.4 (20-40% overhead for cooling, etc.)

**Power distribution**:
1. Utility connection (typically 10-100 kV)
2. Step-down transformers → 480V
3. Uninterruptible Power Supply (UPS): Battery backup (5-15 minutes)
   - Bridges to generator startup
4. Generators: Diesel, natural gas (sustain indefinitely)
5. Distribution: 480V → 208V or direct 480V to racks

**Redundancy**: N+1 or 2N (every component duplicated)
- Power: Multiple utility feeds, multiple UPS units, multiple generators
- Cooling: Redundant chillers, pumps, CRAC units
- Network: Multiple fiber connections, redundant switches

**Cooling**: ~40% of total power consumption
- Traditional: Computer Room Air Conditioning (CRAC) units
- Modern: Hot/cold aisle containment, liquid cooling, free cooling (outside air when cold)
- Google: PUE 1.10 (industry-leading)

**Why efficient power critical**: $100M/year electricity costs at scale
- 1% efficiency improvement = $1M/year saved
- Drives innovation in power supplies, cooling, processor efficiency

## Key Terms

| Term | Definition |
|------|------------|
| **Voltage** | Electrical potential difference; energy per charge |
| **Current** | Rate of charge flow (Amperes) |
| **Resistance** | Opposition to current flow (Ohms) |
| **Ohm's Law** | V = IR |
| **AC** | Alternating current; reverses periodically |
| **DC** | Direct current; constant over time |
| **Transformer** | Changes AC voltage via electromagnetic induction |
| **Semiconductor** | Material with controllable conductivity |
| **Diode** | One-way valve for current (PN junction) |
| **Transistor** | Electrically-controlled switch; basis of computing |
| **Integrated circuit** | Multiple components on single chip |
| **Amplifier** | Increases signal amplitude |
| **Modulation** | Encoding information onto carrier wave |
| **Feedback control** | Uses output measurement to adjust input |

## Summary

Electrical engineering harnesses electromagnetic phenomena to generate, transmit, and utilize power. AC power systems with transformers enable efficient long-distance transmission from generating plants to consumers. Three-phase power, high voltages, and the smart grid with distributed generation and storage are transforming how electricity is produced and consumed.

Electronics manipulates electrons in semiconductors—diodes providing rectification, transistors enabling switching and amplification. The transistor's invention revolutionized electronics, evolving from vacuum tubes to billions of transistors on integrated circuits following Moore's Law for 50+ years. Digital logic gates built from transistors create computers; microprocessors integrate billions of switches performing billions of operations per second.

Analog electronics amplifies signals, filters noise, and converts between analog and digital domains. Communication systems modulate information onto electromagnetic waves, enabling wireless communication from AM radio to 5G cellular to fiber optic cables carrying terabits across oceans. Control systems use feedback to maintain desired outputs despite disturbances—from cruise control to industrial automation.

Modern devices—smartphones with 15 billion transistors and dozens of sensors, electric vehicles with power electronics managing 300 kW, data centers consuming 100 MW—demonstrate electrical and electronics engineering's central role. From the power grid energizing civilization to the semiconductor chips processing information, electrical engineering remains the foundation of modern technology.

# AtmoSync Micro-Climate Analytics & Thermal Kinetics Specification

## 1. Arrhenius Quality Degradation Kinetics Formula

$$\text{Reaction Rate } k(T) = A \cdot \exp\left(-\frac{E_a}{R \cdot T}\right)$$

Where:
- $E_a$: Activation Energy for commodity degradation ($\text{kJ/mol}$)
- $R$: Universal Gas Constant ($8.314 \, \text{J/(mol} \cdot \text{K)}$)
- $T$: Absolute Temperature ($\text{Kelvin} = T_{^\circ\text{C}} + 273.15$)

### Quality Decay Ratio ($Q_{decay}$):
$$Q_{decay} = \frac{k(T_{current})}{k(T_{optimum})}$$

## 2. Remaining Shelf Life (RSL) Calculation

$$\text{RSL (Days)} = \max\left(0, \text{Base Shelf Life} - (\text{Days Passed} \cdot Q_{decay})\right)$$

## 3. Net Arbitrage Profit Delta Formula

$$\text{Net Delta} = \text{Revenue}_{\text{alt}} - \text{Revenue}_{\text{primary}} - \text{Reroute Transport Cost}$$

$$\text{Reroute Cost} = |\Delta \text{Distance}_{\text{km}}| \times \$1.85/\text{km} + \$500 \text{ (Port Diversion Fee)}$$

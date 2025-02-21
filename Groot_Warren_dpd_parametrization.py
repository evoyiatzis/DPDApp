import numpy as np
import pandas as pd
import streamlit as st

st.header("Parametrization of DPD models using the Groot - De Warren approach")

st.text("This is a WebApp for the parametrization of DPD models using the Groot De Warren methodology. "
        "The reference is 'Dissipative particle dynamics: "
        "Bridging the gap between atomistic and mesoscopic simulation' "
        "J. Chem. Phys. DOI:10.1063/1.474784")

st.text("This WebApp was created by Evangelos Voyiatzis.")

with st.form("my_form"):
    st.write("System Properties")
    temperature = st.text_input("Temperature in DPD units usually 1.0 [float]")
    density = st.text_input("Number density in DPD units usually 3.0 [float]")
    number = st.text_input("Number of DPD bead types in the system [integer]")
    selected_formula = st.radio("Choose formula for cross parameters:", [r"$\rho=3.0$", r"$\rho=5.0$"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            temperature = float(temperature)
            if temperature > 0:
                st.write("The temperature is:", temperature)
                st.session_state['temperature'] = temperature
            else:
                st.write("The temperature should be greater than zero")
        except ValueError:
            st.write("You have not entered a valid temperature")

        try:
            density = float(density)
            if density > 0:
                st.write("The number density is:", density)
                st.session_state['density'] = density
            else:
                st.write("The density should be greater than zero")
        except ValueError:
            st.write("You have not entered a valid density")

        try:
            number = int(number)
            if number > 0:
                st.write("The number of DPD bead types is:", number)
                st.session_state['number'] = number
            else:
                st.write("The number of DPD bead types should be greater than zero")
        except ValueError:
            st.write("You have not entered a valid number of DPD bead types")

if all(x in st.session_state for x in ['number', 'temperature', 'density']):
    with st.form("second_form"):
        st.write("Flory–Huggins parameters")

        df = pd.DataFrame(0, index = np.arange(1, number+1, 1), columns=np.arange(1, number+1,1))
        edited_df = st.data_editor(df)

        submit = st.form_submit_button("Submit")

if submit in st.session_state:
    with st.container(border=True):
        st.write("DPD interaction parameters")

        # set the diagonal terms
        for i in range(0, number):
            edited_df.iloc[i,i] = 75.0 * temperature / density

        # set the off-diagonal terms

        st.dataframe(edited_df)

        pressure = density * temperature + 0.101 * np.power(density, 3) * edited_df.iloc[0,0]
        st.write("The expected pressure in DPD units is:", pressure)

if st.button("Reset"):
    if 'number' in st.session_state:
        del st.session_state['number']
    if 'temperature' in st.session_state:
        del st.session_state['temperature']
    if 'density' in st.session_state:
        del st.session_state['density']
    if 'submit' in st.session_state:
        del st.session_state['submit']

    st.rerun()

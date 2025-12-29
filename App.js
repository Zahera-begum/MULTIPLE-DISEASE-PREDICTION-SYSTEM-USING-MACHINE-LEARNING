import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isRegister, setIsRegister] = useState(false);
  const [authData, setAuthData] = useState({ username: '', password: '' });
  const [disease, setDisease] = useState('heart');
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [chat, setChat] = useState({ q: '', a: '' });
  const [feedback, setFeedback] = useState('');

  const fieldIcons = {
    Age: '👤', Sex: '🚻', ChestPain: '💔', RestBP: '📉', Cholesterol: '🍔', FBS: '🍬', RestECG: '📟', MaxHR: '⚡',
    Gender: '🚻', Total_Bilirubin: '🧪', Alkaline_Phosphotase: '🔬', Alamine_Aminotransferase: '🧬', Albumin: '🥚',
    Pregnancies: '🤰', Glucose: '🍭', BloodPressure: '🩺', SkinThickness: '📏', Insulin: '💉', BMI: '⚖️'
  };

  const inputConfig = {
    heart: ['Age', 'Sex', 'ChestPain', 'RestBP', 'Cholesterol', 'FBS', 'RestECG', 'MaxHR'],
    liver: ['Age', 'Gender', 'Total_Bilirubin', 'Alkaline_Phosphotase', 'Alamine_Aminotransferase', 'Albumin'],
    diabetes: ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Age']
  };

  const containerStyle = {
    backgroundImage: `linear-gradient(rgba(10, 20, 40, 0.75), rgba(10, 20, 40, 0.75)), url(${process.env.PUBLIC_URL + '/background.jpg'})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundAttachment: 'fixed',
    minHeight: '100vh'
  };

  const handleAuth = async () => {
    try {
      const url = isRegister ? 'register/' : 'login/';
      const res = await axios.post(`http://127.0.0.1:8000/api/${url}`, authData);
      if (!isRegister) {
        localStorage.setItem('token', res.data.access);
        setToken(res.data.access);
      } else {
        alert("✅ Account Ready! Please Login.");
        setIsRegister(false);
      }
    } catch (err) { alert("❌ Login Failed"); }
  };

  const handlePredict = async () => {
    const vals = inputConfig[disease].map(f => parseFloat(formData[f]) || 0);
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/predict/', 
        { type: disease, medical_data: vals },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(res.data);
    } catch (err) { alert("⚠️ Analysis Failed"); }
  };

  if (!token) {
    return (
      <div className="main-container" style={containerStyle}>
        <div className="glass-card" style={{maxWidth:'380px'}}>
          <h2 style={{textAlign:'center'}}>🔐 Hospital Login</h2>
          <input style={{width:'100%', boxSizing:'border-box', marginBottom:'10px'}} type="text" placeholder="Username" onChange={e => setAuthData({...authData, username: e.target.value})} />
          <input style={{width:'100%', boxSizing:'border-box', marginBottom:'20px'}} type="password" placeholder="Password" onChange={e => setAuthData({...authData, password: e.target.value})} />
          <button className="analyze-btn" onClick={handleAuth}>{isRegister ? "Create Account" : "Login"}</button>
          <p onClick={() => setIsRegister(!isRegister)} style={{cursor:'pointer', textAlign:'center', marginTop:'15px', fontSize:'13px', color:'#94a3b8'}}>
            {isRegister ? "Already a member? Login" : "New Patient? Join here"}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="main-container" style={containerStyle}>
      <div className="glass-card">
        <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'30px'}}>
          <h1 style={{margin:0}}>🏥 HealthCheck AI</h1>
          <button onClick={() => {localStorage.clear(); setToken(null);}} style={{background:'rgba(255,255,255,0.1)', color:'white', border:'none', padding:'8px 15px', borderRadius:'10px', cursor:'pointer'}}>Exit 🚪</button>
        </div>

        <div className="selector">
          <button className={disease === 'heart' ? "active" : ""} onClick={() => {setDisease('heart'); setResult(null);}}>❤️ HEART</button>
          <button className={disease === 'liver' ? "active" : ""} onClick={() => {setDisease('liver'); setResult(null);}}>🧪 LIVER</button>
          <button className={disease === 'diabetes' ? "active" : ""} onClick={() => {setDisease('diabetes'); setResult(null);}}>🩸 DIABETES</button>
        </div>

        <div className="input-grid">
          {inputConfig[disease].map(f => (
            <div key={f} className="input-wrapper">
              <label>{fieldIcons[f] || '🔹'} {f.toUpperCase()}</label>
              <input placeholder="0.0" type="number" onChange={e => setFormData({...formData, [f]: e.target.value})} />
            </div>
          ))}
        </div>

        <button className="analyze-btn" onClick={handlePredict}>🔍 RUN ANALYSIS</button>

        {result && (
          <div className={`result-box ${result.risk_status === 'High Risk' ? 'high' : 'low'}`}>
            <h2 style={{margin:0}}>{result.risk_status === 'High Risk' ? '🚨' : '✅'} {result.risk_status}</h2>
            <p style={{margin:'10px 0'}}>💡 {result.recommendation}</p>
            {result.hospitals.map(h => (
              <div key={h.name} className="hospital-item">
                <strong>🏥 {h.name}</strong> <span>📞 {h.contact}</span>
              </div>
            ))}
          </div>
        )}

        <div className="chat-feedback-grid">
          <div className="utility-box">
            <h4 style={{marginTop:0}}>🤖 AI Help</h4>
            <div style={{display:'flex', gap:'5px'}}>
              <input style={{flex:1}} placeholder="Ask health tips..." value={chat.q} onChange={e => setChat({...chat, q: e.target.value})} />
              <button className="analyze-btn" style={{padding:'5px 12px', width:'auto', fontSize:'12px'}} onClick={async () => {
                const res = await axios.post('http://127.0.0.1:8000/api/chatbot/', {query: chat.q}, {headers: {Authorization: `Bearer ${token}`}});
                setChat({...chat, a: res.data.reply});
              }}>ASK</button>
            </div>
            {chat.a && <p style={{fontSize:'12px', color:'#0ea5e9', marginTop:'10px'}}>👨‍⚕️: {chat.a}</p>}
          </div>

          <div className="utility-box">
            <h4 style={{marginTop:0}}>✍️ Feedback</h4>
            <textarea className="feedback-textarea" placeholder="Experience..." onChange={e => setFeedback(e.target.value)} />
            <button className="analyze-btn" style={{padding:'5px', width:'100%', marginTop:'5px', fontSize:'12px'}} onClick={async () => {
              await axios.post('http://127.0.0.1:8000/api/feedback/', {message: feedback}, {headers: {Authorization: `Bearer ${token}`}});
              alert("🙏 Thanks!");
            }}>SUBMIT</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
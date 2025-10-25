import React, {useState, useEffect} from 'react'

const API = 'http://localhost:5000/api'

export default function App(){
  const [token, setToken] = useState(localStorage.getItem('token')||'')
  const [username, setUsername] = useState('')
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState([])
  const [form, setForm] = useState({username:'',password:''})

  useEffect(()=>{ if(token) fetchProducts() },[token])

  async function register(){
    const res = await fetch(API+'/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(form)})
    const j = await res.json()
    if(j.token){ localStorage.setItem('token', j.token); setToken(j.token); setUsername(j.username) }
    else alert(j.message||'error')
  }

  async function login(){
    const res = await fetch(API+'/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(form)})
    const j = await res.json()
    if(j.token){ localStorage.setItem('token', j.token); setToken(j.token); setUsername(j.username) }
    else alert(j.message||'error')
  }

  async function fetchProducts(){
    const res = await fetch(API+'/products',{headers:{'Authorization':'Bearer '+token}})
    const j = await res.json()
    setProducts(j)
  }

  function addToCart(p){
    const exists = cart.find(i=>i.product_id===p.id)
    if(exists){ setCart(cart.map(i=> i.product_id===p.id ? {...i, qty:i.qty+1} : i)) }
    else setCart([...cart,{product_id:p.id,qty:1,name:p.name,price:p.price}])
  }

  async function checkout(){
    const res = await fetch(API+'/checkout',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},body:JSON.stringify({items:cart})})
    const j = await res.json()
    if(j.order_id){ alert('Order placed: '+j.order_id); setCart([]); fetchProducts() }
    else alert(j.message||'error')
  }

  return (
    <div style={{padding:20}}>
      <h2>sukistore (beta)</h2>
      {!token ? (
        <div>
          <input placeholder='username' value={form.username} onChange={e=>setForm({...form,username:e.target.value})}/>
          <input placeholder='password' type='password' value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>
          <button onClick={register}>Register</button>
          <button onClick={login}>Login</button>
        </div>
      ) : (
        <div>
          <div>Halo, {username}</div>
          <button onClick={()=>{localStorage.removeItem('token'); setToken('')}}>Logout</button>
        </div>
      )}
      <hr/>
      <h3>Produk</h3>
      {products.map(p=>(
        <div key={p.id} style={{border:'1px solid #ccc',padding:10,marginBottom:8}}>
          <div>{p.name}</div>
          <div>Rp {p.price}</div>
          <div>Stok: {p.stock}</div>
          <button onClick={()=>addToCart(p)}>Tambah ke keranjang</button>
        </div>
      ))}
      <hr/>
      <h3>Keranjang</h3>
      {cart.map(i=><div key={i.product_id}>{i.name} x{i.qty} - Rp {i.price*i.qty}</div>)}
      <button onClick={checkout} disabled={cart.length===0}>Checkout</button>
    </div>
  )
}

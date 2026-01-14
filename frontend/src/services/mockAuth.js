/**
 * Mock Authentication Service
 * Used when backend is not available (deployed frontend without backend)
 */

const MOCK_USERS = {
  'admin@verisignal.com': {
    id: 1,
    email: 'admin@verisignal.com',
    username: 'admin',
    name: 'Admin User',
    full_name: 'Admin User',
    company: 'VeriSignal',
    role: 'admin',
    password: 'admin123',
    is_active: true
  },
  'admin@reputation.ai': {
    id: 2,
    email: 'admin@reputation.ai',
    username: 'admin',
    name: 'System Administrator',
    full_name: 'System Administrator',
    role: 'admin',
    password: 'Admin@2024!',
    is_active: true
  },
  'user@verisignal.com': {
    id: 3,
    email: 'user@verisignal.com',
    username: 'user',
    name: 'Demo User',
    full_name: 'Demo User',
    company: 'Demo Corp',
    role: 'user',
    password: 'user123',
    is_active: true
  }
};

export const mockAuthService = {
  login: async (email, password) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const user = MOCK_USERS[email];
    
    if (!user || user.password !== password) {
      throw new Error('Invalid email or password');
    }
    
    // Create mock token
    const token = btoa(JSON.stringify({ user_id: user.id, email: user.email, exp: Date.now() + 86400000 }));
    
    // Return user data without password
    const { password: _, ...userData } = user;
    
    return {
      data: {
        token,
        user: userData
      }
    };
  },
  
  register: async (data) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    throw new Error('Registration is disabled in demo mode. Please use one of the provided accounts.');
  },
  
  getCurrentUser: async () => {
    await new Promise(resolve => setTimeout(resolve, 200));
    return {
      data: MOCK_USERS['admin@reputation.ai']
    };
  },
  
  logout: async () => {
    await new Promise(resolve => setTimeout(resolve, 200));
    return { data: { message: 'Logged out successfully' } };
  }
};

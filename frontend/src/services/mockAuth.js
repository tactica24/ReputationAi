/**
 * Mock Authentication Service
 * Used when backend is not available (deployed frontend without backend)
 */

const MOCK_USERS = {
  'admin@reputation.ai': {
    id: 1,
    email: 'admin@reputation.ai',
    username: 'admin',
    full_name: 'System Administrator',
    role: 'super_admin',
    password: 'Admin@2024!',
    is_active: true
  },
  'manager@reputation.ai': {
    id: 2,
    email: 'manager@reputation.ai',
    username: 'manager',
    full_name: 'Demo Manager',
    role: 'manager',
    password: 'Manager@2024!',
    is_active: true
  },
  'analyst@reputation.ai': {
    id: 3,
    email: 'analyst@reputation.ai',
    username: 'analyst',
    full_name: 'Demo Analyst',
    role: 'analyst',
    password: 'Analyst@2024!',
    is_active: true
  },
  'user@reputation.ai': {
    id: 4,
    email: 'user@reputation.ai',
    username: 'viewer',
    full_name: 'Demo Viewer',
    role: 'viewer',
    password: 'User@2024!',
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

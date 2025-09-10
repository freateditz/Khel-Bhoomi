import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Badge } from "./components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "./components/ui/avatar";
import { Textarea } from "./components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { useToast } from "./hooks/use-toast";
import { Toaster } from "./components/ui/sonner";
import { 
  Users, 
  Trophy, 
  Target, 
  Heart, 
  MessageCircle, 
  Share2, 
  Plus,
  Search,
  Bell,
  Settings,
  LogOut,
  Camera,
  Video,
  Award
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Authentication Context
const AuthContext = React.createContext();

const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      // Set default authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Get user profile
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get(`${API}/users/me`);
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = (tokenData) => {
    localStorage.setItem('token', tokenData.access_token);
    setToken(tokenData.access_token);
    setUser(tokenData.user);
    axios.defaults.headers.common['Authorization'] = `Bearer ${tokenData.access_token}`;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

// Landing Page Component
const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background with Grid Pattern */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
        <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-white/80 via-transparent to-transparent"></div>
      </div>
      
      {/* Hero Section */}
      <div className="relative z-10">
        <nav className="flex items-center justify-between p-6">
          <div className="flex items-center space-x-2">
            <Trophy className="h-8 w-8 text-orange-500" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
              Khel Bhoomi
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button variant="ghost" className="text-slate-700 hover:text-orange-500">
              About
            </Button>
            <Button variant="ghost" className="text-slate-700 hover:text-orange-500">
              Features
            </Button>
            <Button variant="outline" className="border-orange-200 text-orange-600 hover:bg-orange-50" onClick={() => navigate('/auth')}>
              Login
            </Button>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white" onClick={() => navigate('/auth')}>
              Sign Up
            </Button>
          </div>
        </nav>

        {/* Main Hero Content */}
        <div className="container mx-auto px-6 pt-20 pb-32">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-6xl font-bold text-slate-900 mb-6 leading-tight">
              Connect, Compete, and
              <span className="bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent block">
                Conquer Sports
              </span>
            </h1>
            
            <p className="text-xl text-slate-600 mb-12 max-w-2xl mx-auto leading-relaxed">
              The ultimate sports social platform where athletes showcase talent, scouts discover champions, 
              and fans celebrate the spirit of sports together.
            </p>

            <div className="flex items-center justify-center space-x-6 mb-16">
              <Button 
                size="lg" 
                className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 text-lg rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <Trophy className="h-5 w-5 mr-2" />
                Explore Feed
              </Button>
              
              <Button 
                size="lg" 
                variant="outline" 
                className="border-2 border-orange-200 text-orange-600 hover:bg-orange-50 px-8 py-4 text-lg rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <Users className="h-5 w-5 mr-2" />
                Join Community
              </Button>
            </div>

            {/* Role Selection Cards */}
            <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              <Card className="glass-card group hover:scale-105 transition-all duration-300 border-0 shadow-xl">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <Trophy className="h-8 w-8 text-white" />
                  </div>
                  <CardTitle className="text-xl font-bold text-slate-800">Athletes</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-slate-600 mb-4">
                    Showcase your achievements, share training updates, and connect with scouts.
                  </p>
                  <Button className="w-full bg-blue-500 hover:bg-blue-600 text-white">
                    Join as Athlete
                  </Button>
                </CardContent>
              </Card>

              <Card className="glass-card group hover:scale-105 transition-all duration-300 border-0 shadow-xl">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <Target className="h-8 w-8 text-white" />
                  </div>
                  <CardTitle className="text-xl font-bold text-slate-800">Scouts</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-slate-600 mb-4">
                    Discover emerging talent, evaluate players, and build winning teams.
                  </p>
                  <Button className="w-full bg-green-500 hover:bg-green-600 text-white">
                    Join as Scout
                  </Button>
                </CardContent>
              </Card>

              <Card className="glass-card group hover:scale-105 transition-all duration-300 border-0 shadow-xl">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <Heart className="h-8 w-8 text-white" />
                  </div>
                  <CardTitle className="text-xl font-bold text-slate-800">Fans</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-slate-600 mb-4">
                    Follow your favorite athletes, discuss matches, and celebrate victories.
                  </p>
                  <Button className="w-full bg-purple-500 hover:bg-purple-600 text-white">
                    Join as Fan
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* Sports Images Section */}
        <div className="relative">
          <div className="container mx-auto px-6 py-16">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="glass-card overflow-hidden group">
                <img 
                  src="https://images.unsplash.com/photo-1608245449230-4ac19066d2d0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxhdGhsZXRlfGVufDB8fHx8MTc1NzUzMTYxMnww&ixlib=rb-4.1.0&q=85" 
                  alt="Basketball" 
                  className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="p-4">
                  <h3 className="font-semibold text-slate-800">Elite Basketball</h3>
                  <p className="text-sm text-slate-600">High-performance training and competition</p>
                </div>
              </div>

              <div className="glass-card overflow-hidden group">
                <img 
                  src="https://images.unsplash.com/photo-1461896836934-ffe607ba8211?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdGhsZXRlfGVufDB8fHx8MTc1NzUzMTYxMnww&ixlib=rb-4.1.0&q=85" 
                  alt="Track and Field" 
                  className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="p-4">
                  <h3 className="font-semibold text-slate-800">Track & Field</h3>
                  <p className="text-sm text-slate-600">Speed, endurance, and athletic excellence</p>
                </div>
              </div>

              <div className="glass-card overflow-hidden group">
                <img 
                  src="https://images.unsplash.com/photo-1697767394715-75e8183e85bb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxzcG9ydHMlMjBjb21tdW5pdHl8ZW58MHx8fHwxNzU3NTMxNjA1fDA&ixlib=rb-4.1.0&q=85" 
                  alt="Soccer Community" 
                  className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="p-4">
                  <h3 className="font-semibold text-slate-800">Football Community</h3>
                  <p className="text-sm text-slate-600">Global sport, local communities</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Authentication Component
const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'fan'
  });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const payload = isLogin 
        ? { username: formData.username, password: formData.password }
        : formData;

      const response = await axios.post(`${API}${endpoint}`, payload);
      login(response.data);
      toast({
        title: isLogin ? "Welcome back!" : "Account created successfully!",
        description: `Logged in as ${response.data.user.username}`
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Something went wrong",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 p-4">
      <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
      
      <Card className="w-full max-w-md glass-card border-0 shadow-2xl relative z-10">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Trophy className="h-8 w-8 text-orange-500" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
              Khel Bhoomi
            </h1>
          </div>
          <CardTitle className="text-2xl font-bold text-slate-800">
            {isLogin ? 'Welcome Back' : 'Join the Community'}
          </CardTitle>
          <CardDescription className="text-slate-600">
            {isLogin ? 'Sign in to your account' : 'Create your sports profile'}
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="username" className="text-slate-700">Username</Label>
              <Input
                id="username"
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                required
                className="mt-1"
              />
            </div>

            {!isLogin && (
              <>
                <div>
                  <Label htmlFor="email" className="text-slate-700">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    required
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="full_name" className="text-slate-700">Full Name</Label>
                  <Input
                    id="full_name"
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                    required
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="role" className="text-slate-700">I am a...</Label>
                  <Select value={formData.role} onValueChange={(value) => setFormData({...formData, role: value})}>
                    <SelectTrigger className="mt-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="athlete">Athlete</SelectItem>
                      <SelectItem value="scout">Scout</SelectItem>
                      <SelectItem value="fan">Sports Fan</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </>
            )}

            <div>
              <Label htmlFor="password" className="text-slate-700">Password</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
                className="mt-1"
              />
            </div>

            <Button 
              type="submit" 
              className="w-full bg-orange-500 hover:bg-orange-600 text-white"
              disabled={loading}
            >
              {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
            </Button>

            <p className="text-center text-sm text-slate-600">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                className="text-orange-500 hover:text-orange-600 font-medium"
              >
                {isLogin ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

// Feed Component
const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ content: '', post_type: 'text', sports_tags: [] });
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const { toast } = useToast();

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get(`${API}/posts`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const createPost = async () => {
    if (!newPost.content.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/posts`, newPost);
      setPosts([response.data, ...posts]);
      setNewPost({ content: '', post_type: 'text', sports_tags: [] });
      toast({
        title: "Post created!",
        description: "Your post has been shared with the community."
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create post",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'athlete': return 'bg-blue-100 text-blue-800';
      case 'scout': return 'bg-green-100 text-green-800';
      case 'fan': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'athlete': return <Trophy className="h-3 w-3" />;
      case 'scout': return <Target className="h-3 w-3" />;
      case 'fan': return <Heart className="h-3 w-3" />;
      default: return null;
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-6">
      {/* Create Post Card */}
      <Card className="glass-card border-0 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-start space-x-4">
            <Avatar>
              <AvatarFallback className="bg-orange-100 text-orange-600">
                {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            
            <div className="flex-1 space-y-4">
              <Textarea
                placeholder={`What's happening in sports, ${user?.full_name?.split(' ')[0] || user?.username}?`}
                value={newPost.content}
                onChange={(e) => setNewPost({...newPost, content: e.target.value})}
                className="border-0 resize-none focus:ring-0 text-lg placeholder:text-slate-400"
                rows={3}
              />
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Button variant="ghost" size="sm" className="text-slate-500 hover:text-orange-500">
                    <Camera className="h-4 w-4 mr-1" />
                    Photo
                  </Button>
                  <Button variant="ghost" size="sm" className="text-slate-500 hover:text-orange-500">
                    <Video className="h-4 w-4 mr-1" />
                    Video
                  </Button>
                  <Button variant="ghost" size="sm" className="text-slate-500 hover:text-orange-500">
                    <Award className="h-4 w-4 mr-1" />
                    Achievement
                  </Button>
                </div>
                
                <Button 
                  onClick={createPost}
                  disabled={loading || !newPost.content.trim()}
                  className="bg-orange-500 hover:bg-orange-600 text-white rounded-full px-6"
                >
                  {loading ? 'Posting...' : 'Post'}
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Posts Feed */}
      <div className="space-y-4">
        {posts.map((post) => (
          <Card key={post.id} className="glass-card border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardContent className="p-6">
              <div className="flex items-start space-x-4">
                <Avatar>
                  <AvatarFallback className="bg-slate-100 text-slate-600">
                    {post.username?.charAt(0)}
                  </AvatarFallback>
                </Avatar>
                
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h4 className="font-semibold text-slate-800">{post.username}</h4>
                    <Badge className={`text-xs px-2 py-1 ${getRoleColor(post.user_role)}`}>
                      <span className="flex items-center space-x-1">
                        {getRoleIcon(post.user_role)}
                        <span className="capitalize">{post.user_role}</span>
                      </span>
                    </Badge>
                    <span className="text-sm text-slate-500">
                      {new Date(post.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  
                  <p className="text-slate-700 mb-4 leading-relaxed">{post.content}</p>
                  
                  {post.image_url && (
                    <div className="mb-4 rounded-lg overflow-hidden">
                      <img 
                        src={post.image_url} 
                        alt="Post content" 
                        className="w-full h-auto max-h-96 object-cover"
                      />
                    </div>
                  )}
                  
                  {post.sports_tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {post.sports_tags.map((tag, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          #{tag}
                        </Badge>
                      ))}
                    </div>
                  )}
                  
                  <div className="flex items-center space-x-6 text-slate-500">
                    <Button variant="ghost" size="sm" className="hover:text-red-500 hover:bg-red-50">
                      <Heart className="h-4 w-4 mr-1" />
                      {post.likes}
                    </Button>
                    <Button variant="ghost" size="sm" className="hover:text-blue-500 hover:bg-blue-50">
                      <MessageCircle className="h-4 w-4 mr-1" />
                      {post.comments}
                    </Button>
                    <Button variant="ghost" size="sm" className="hover:text-green-500 hover:bg-green-50">
                      <Share2 className="h-4 w-4 mr-1" />
                      Share
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

// Main Dashboard Component
const Dashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('feed');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
      
      {/* Top Navigation */}
      <nav className="relative z-10 bg-white/70 backdrop-blur-lg border-b border-white/20 shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <div className="flex items-center space-x-2">
                <Trophy className="h-8 w-8 text-orange-500" />
                <h1 className="text-xl font-bold bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
                  Khel Bhoomi
                </h1>
              </div>
              
              <div className="hidden md:flex items-center space-x-6">
                <Button 
                  variant={activeTab === 'feed' ? 'default' : 'ghost'} 
                  onClick={() => setActiveTab('feed')}
                  className={activeTab === 'feed' ? 'bg-orange-500 hover:bg-orange-600 text-white' : 'text-slate-600 hover:text-orange-500'}
                >
                  Feed
                </Button>
                <Button 
                  variant="ghost" 
                  className="text-slate-600 hover:text-orange-500"
                >
                  Explore
                </Button>
                <Button 
                  variant="ghost" 
                  className="text-slate-600 hover:text-orange-500"
                >
                  Messages
                </Button>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" className="text-slate-600 hover:text-orange-500">
                <Search className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="sm" className="text-slate-600 hover:text-orange-500">
                <Bell className="h-5 w-5" />
              </Button>
              
              <div className="flex items-center space-x-2">
                <Avatar className="h-8 w-8">
                  <AvatarFallback className="bg-orange-100 text-orange-600 text-sm">
                    {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
                  </AvatarFallback>
                </Avatar>
                <span className="hidden md:block text-sm font-medium text-slate-700">
                  {user?.full_name || user?.username}
                </span>
              </div>
              
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={logout}
                className="text-slate-600 hover:text-red-500"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto py-8">
        {activeTab === 'feed' && <Feed />}
      </div>
      
      <Toaster />
    </div>
  );
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Trophy className="h-12 w-12 text-orange-500 mx-auto mb-4 animate-spin" />
          <p className="text-slate-600">Loading...</p>
        </div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/auth" />;
};

// Main App Component
function App() {
  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </BrowserRouter>
        <Toaster />
      </div>
    </AuthProvider>
  );
}

export default App;
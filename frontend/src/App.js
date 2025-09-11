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
  Award,
  User,
  Home,
  Edit,
  MapPin,
  Calendar,
  Star,
  MoreHorizontal,
  Send,
  BookOpen,
  TrendingUp,
  UserCheck,
  Medal
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

// Features Page Component
const FeaturesPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100">
      <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
      
      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between p-6 backdrop-blur-lg bg-white/70 border-b border-purple-100/50">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
          <div className="p-2 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl shadow-lg">
            <Trophy className="h-8 w-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Khel Bhoomi
            </h1>
            <p className="text-xs text-purple-500 font-medium">Sports Community</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={() => navigate('/')}>Home</Button>
          <Button variant="ghost" onClick={() => navigate('/about')}>About</Button>
          <Button onClick={() => navigate('/auth')}>Join Now</Button>
        </div>
      </nav>

      {/* Features Content */}
      <div className="relative z-10 container mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-slate-800 mb-6">Powerful Features</h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Everything you need to excel in sports, connect with like-minded individuals, and showcase your talent to the world.
          </p>
        </div>

        {/* Feature Categories */}
        <div className="grid lg:grid-cols-3 gap-8 mb-16">
          {/* For Athletes */}
          <Card className="glass-card border-0 shadow-xl">
            <CardHeader>
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-4">
                <Trophy className="h-8 w-8 text-white" />
              </div>
              <CardTitle className="text-2xl">For Athletes</CardTitle>
              <CardDescription>Showcase your talent and get discovered</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Digital Portfolio</h4>
                  <p className="text-sm text-slate-600">Create comprehensive profiles with achievements, stats, and videos</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Performance Tracking</h4>
                  <p className="text-sm text-slate-600">Track your progress, set goals, and monitor improvements</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Scout Connections</h4>
                  <p className="text-sm text-slate-600">Get discovered by professional scouts and recruiters</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* For Scouts */}
          <Card className="glass-card border-0 shadow-xl">
            <CardHeader>
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mb-4">
                <Target className="h-8 w-8 text-white" />
              </div>
              <CardTitle className="text-2xl">For Scouts</CardTitle>
              <CardDescription>Discover and evaluate emerging talent</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Talent Database</h4>
                  <p className="text-sm text-slate-600">Access comprehensive database of athletes with detailed profiles</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Advanced Filters</h4>
                  <p className="text-sm text-slate-600">Search by sport, location, age, skill level, and achievements</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Direct Communication</h4>
                  <p className="text-sm text-slate-600">Connect directly with athletes and their representatives</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* For Fans */}
          <Card className="glass-card border-0 shadow-xl">
            <CardHeader>
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-4">
                <Heart className="h-8 w-8 text-white" />
              </div>
              <CardTitle className="text-2xl">For Fans</CardTitle>
              <CardDescription>Follow and support your favorite athletes</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Follow Athletes</h4>
                  <p className="text-sm text-slate-600">Stay updated with your favorite athletes' journeys and achievements</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Community Discussions</h4>
                  <p className="text-sm text-slate-600">Engage in sports discussions and celebrate victories together</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-semibold">Live Updates</h4>
                  <p className="text-sm text-slate-600">Get real-time updates on matches, tournaments, and events</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Technical Features */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-slate-800 mb-4">Technical Excellence</h2>
          <p className="text-xl text-slate-600">Built with modern technology for the best user experience</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { icon: <MessageCircle className="h-8 w-8" />, title: "Real-time Chat", desc: "Instant messaging between athletes and scouts" },
            { icon: <Camera className="h-8 w-8" />, title: "Media Upload", desc: "Share photos and videos of your achievements" },
            { icon: <Bell className="h-8 w-8" />, title: "Smart Notifications", desc: "Never miss important updates or opportunities" },
            { icon: <Search className="h-8 w-8" />, title: "Advanced Search", desc: "Find exactly what you're looking for with powerful filters" }
          ].map((feature, index) => (
            <Card key={index} className="glass-card border-0 shadow-lg text-center">
              <CardContent className="p-6">
                <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">{feature.title}</h3>
                <p className="text-slate-600 text-sm">{feature.desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

// About Page Component  
const AboutPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100">
      <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
      
      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between p-6 backdrop-blur-lg bg-white/70 border-b border-purple-100/50">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
          <div className="p-2 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl shadow-lg">
            <Trophy className="h-8 w-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Khel Bhoomi
            </h1>
            <p className="text-xs text-purple-500 font-medium">Sports Community</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={() => navigate('/')}>Home</Button>
          <Button variant="ghost" onClick={() => navigate('/features')}>Features</Button>
          <Button onClick={() => navigate('/auth')}>Join Now</Button>
        </div>
      </nav>

      {/* About Content */}
      <div className="relative z-10 container mx-auto px-6 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-slate-800 mb-6">About Khel Bhoomi</h1>
          <p className="text-2xl text-slate-600 max-w-4xl mx-auto leading-relaxed">
            We're on a mission to revolutionize Indian sports by connecting talented athletes with professional scouts and passionate fans, creating opportunities that transform lives.
          </p>
        </div>

        {/* Mission & Vision */}
        <div className="grid md:grid-cols-2 gap-12 mb-16">
          <Card className="glass-card border-0 shadow-xl">
            <CardContent className="p-8">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-6">
                <Target className="h-8 w-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-slate-800 mb-4">Our Mission</h2>
              <p className="text-slate-600 text-lg leading-relaxed">
                To democratize sports opportunities in India by providing a platform where talent is recognized regardless of background, location, or connections. We believe every athlete deserves a chance to shine.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-0 shadow-xl">
            <CardContent className="p-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-6">
                <Star className="h-8 w-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-slate-800 mb-4">Our Vision</h2>
              <p className="text-slate-600 text-lg leading-relaxed">
                To become India's premier sports discovery platform, where the next Olympic champion, cricket star, or sporting legend is discovered and nurtured through our community-driven ecosystem.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Story Section */}
        <div className="mb-16">
          <Card className="glass-card border-0 shadow-xl">
            <CardContent className="p-12">
              <div className="text-center mb-8">
                <h2 className="text-4xl font-bold text-slate-800 mb-4">Our Story</h2>
                <p className="text-xl text-slate-600">From idea to India's sports revolution</p>
              </div>
              
              <div className="max-w-4xl mx-auto">
                <p className="text-slate-700 text-lg leading-relaxed mb-6">
                  Khel Bhoomi was born from a simple observation: India has incredible sporting talent, but many athletes struggle to get the recognition and opportunities they deserve. Traditional scouting methods often miss gems hidden in small towns and rural areas.
                </p>
                <p className="text-slate-700 text-lg leading-relaxed mb-6">
                  Founded in 2025, our platform leverages technology to bridge this gap. We've created a space where athletes can showcase their abilities, scouts can discover new talent efficiently, and fans can support the sports ecosystem at every level.
                </p>
                <p className="text-slate-700 text-lg leading-relaxed">
                  Today, we're proud to be home to over 10,000 athletes, 500+ professional scouts, and 50,000+ passionate sports fans, all working together to elevate Indian sports to new heights.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Values Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-slate-800 mb-4">Our Values</h2>
            <p className="text-xl text-slate-600">What drives us every day</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="glass-card border-0 shadow-lg text-center">
              <CardContent className="p-8">
                <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Users className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-4">Inclusivity</h3>
                <p className="text-slate-600">Sports excellence knows no boundaries. We welcome athletes from all backgrounds, regions, and skill levels.</p>
              </CardContent>
            </Card>

            <Card className="glass-card border-0 shadow-lg text-center">
              <CardContent className="p-8">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Trophy className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-4">Excellence</h3>
                <p className="text-slate-600">We strive for excellence in everything we do, from our platform features to the opportunities we create.</p>
              </CardContent>
            </Card>

            <Card className="glass-card border-0 shadow-lg text-center">
              <CardContent className="p-8">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Heart className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-4">Community</h3>
                <p className="text-slate-600">Sports are best when shared. We foster a supportive community that celebrates every achievement.</p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Team Section */}
        <div className="text-center">
          <h2 className="text-4xl font-bold text-slate-800 mb-4">Join Our Mission</h2>
          <p className="text-xl text-slate-600 mb-8 max-w-3xl mx-auto">
            Whether you're an athlete with dreams, a scout seeking talent, or a fan who loves sports, you have a place in our community.
          </p>
          <Button 
            size="lg" 
            className="bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white px-12 py-6 text-xl rounded-2xl shadow-2xl"
            onClick={() => navigate('/auth')}
          >
            <Trophy className="h-6 w-6 mr-3" />
            Be Part of the Revolution
          </Button>
        </div>
      </div>
    </div>
  );
};

// Messages Page Component
const MessagesPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [selectedChat, setSelectedChat] = useState(null);
  const [messageText, setMessageText] = useState('');

  // Mock conversations data
  const conversations = [
    {
      id: 1,
      name: "Sarah Talent Finder",
      role: "scout",
      lastMessage: "I'd love to discuss some opportunities with you!",
      timestamp: "2 min ago",
      unread: 2,
      avatar: "ST",
      online: true
    },
    {
      id: 2, 
      name: "Mumbai Basketball Academy",
      role: "organization",
      lastMessage: "Training camp starts next Monday. Are you interested?",
      timestamp: "1 hour ago",
      unread: 0,
      avatar: "MBA",
      online: false
    },
    {
      id: 3,
      name: "Raj Sports Lover", 
      role: "fan",
      lastMessage: "Great performance in the last match! 🔥",
      timestamp: "3 hours ago", 
      unread: 1,
      avatar: "RS",
      online: true
    },
    {
      id: 4,
      name: "Delhi Sports Club",
      role: "organization", 
      lastMessage: "We have some exciting sponsorship opportunities...",
      timestamp: "Yesterday",
      unread: 0,
      avatar: "DSC",
      online: false
    }
  ];

  const mockMessages = [
    {
      id: 1,
      senderId: 1,
      text: "Hi Alex! I've been following your basketball performances and I'm really impressed.",
      timestamp: "10:30 AM",
      isOwn: false
    },
    {
      id: 2, 
      senderId: user?.id,
      text: "Thank you! That means a lot coming from a professional scout.",
      timestamp: "10:32 AM", 
      isOwn: true
    },
    {
      id: 3,
      senderId: 1,
      text: "I'd love to discuss some opportunities with you! Would you be available for a call this week?",
      timestamp: "10:35 AM",
      isOwn: false
    }
  ];

  const sendMessage = () => {
    if (messageText.trim()) {
      // Mock sending message
      setMessageText('');
    }
  };

  return (
    <div className="h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100 flex">
      {/* Sidebar */}
      <div className="w-80 bg-white/80 backdrop-blur-xl border-r border-purple-100 flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-purple-100">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-slate-800">Messages</h1>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => navigate('/dashboard')}
              className="text-slate-500 hover:text-purple-600"
            >
              ✕
            </Button>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
            <Input 
              placeholder="Search conversations..." 
              className="pl-10 focus:ring-purple-500 focus:border-purple-500"
            />
          </div>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto">
          {conversations.map((conversation) => (
            <div 
              key={conversation.id}
              className={`p-4 border-b border-purple-50 cursor-pointer hover:bg-purple-50 transition-colors ${
                selectedChat?.id === conversation.id ? 'bg-purple-100' : ''
              }`}
              onClick={() => setSelectedChat(conversation)}
            >
              <div className="flex items-start space-x-3">
                <div className="relative">
                  <Avatar className="w-12 h-12">
                    <AvatarFallback className={`${
                      conversation.role === 'scout' ? 'bg-green-100 text-green-600' :
                      conversation.role === 'fan' ? 'bg-purple-100 text-purple-600' :
                      'bg-blue-100 text-blue-600'
                    } font-semibold`}>
                      {conversation.avatar}
                    </AvatarFallback>
                  </Avatar>
                  {conversation.online && (
                    <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                  )}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="font-semibold text-slate-800 truncate">{conversation.name}</h3>
                    <span className="text-xs text-slate-500">{conversation.timestamp}</span>
                  </div>
                  <p className="text-sm text-slate-600 truncate mb-1">{conversation.lastMessage}</p>
                  <div className="flex items-center justify-between">
                    <Badge 
                      variant="secondary" 
                      className={`text-xs ${
                        conversation.role === 'scout' ? 'bg-green-100 text-green-600' :
                        conversation.role === 'fan' ? 'bg-purple-100 text-purple-600' :
                        'bg-blue-100 text-blue-600'
                      }`}
                    >
                      {conversation.role}
                    </Badge>
                    {conversation.unread > 0 && (
                      <Badge className="bg-purple-500 text-white text-xs px-2 py-1">
                        {conversation.unread}
                      </Badge>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {selectedChat ? (
          <>
            {/* Chat Header */}
            <div className="p-6 bg-white/80 backdrop-blur-xl border-b border-purple-100">
              <div className="flex items-center space-x-4">
                <Avatar className="w-12 h-12">
                  <AvatarFallback className={`${
                    selectedChat.role === 'scout' ? 'bg-green-100 text-green-600' :
                    selectedChat.role === 'fan' ? 'bg-purple-100 text-purple-600' :
                    'bg-blue-100 text-blue-600'
                  } font-semibold`}>
                    {selectedChat.avatar}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h2 className="text-xl font-semibold text-slate-800">{selectedChat.name}</h2>
                  <div className="flex items-center space-x-2">
                    <Badge 
                      variant="secondary" 
                      className={`text-xs ${
                        selectedChat.role === 'scout' ? 'bg-green-100 text-green-600' :
                        selectedChat.role === 'fan' ? 'bg-purple-100 text-purple-600' :
                        'bg-blue-100 text-blue-600'
                      }`}
                    >
                      {selectedChat.role}
                    </Badge>
                    {selectedChat.online && (
                      <span className="text-sm text-green-600 flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                        Online
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 p-6 overflow-y-auto space-y-4">
              {mockMessages.map((message) => (
                <div 
                  key={message.id} 
                  className={`flex ${message.isOwn ? 'justify-end' : 'justify-start'}`}
                >
                  <div 
                    className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                      message.isOwn 
                        ? 'bg-gradient-to-r from-purple-500 to-indigo-500 text-white' 
                        : 'bg-white shadow-lg text-slate-800'
                    }`}
                  >
                    <p className="text-sm">{message.text}</p>
                    <p className={`text-xs mt-1 ${
                      message.isOwn ? 'text-purple-100' : 'text-slate-500'
                    }`}>
                      {message.timestamp}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Message Input */}
            <div className="p-6 bg-white/80 backdrop-blur-xl border-t border-purple-100">
              <div className="flex items-center space-x-4">
                <Button variant="ghost" size="sm" className="text-slate-500 hover:text-purple-600">
                  <Camera className="h-5 w-5" />
                </Button>
                <Input 
                  placeholder="Type your message..."
                  value={messageText}
                  onChange={(e) => setMessageText(e.target.value)}
                  className="flex-1 focus:ring-purple-500 focus:border-purple-500"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      sendMessage();
                    }
                  }}
                />
                <Button 
                  onClick={sendMessage}
                  className="bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <MessageCircle className="h-16 w-16 text-slate-400 mx-auto mb-4" />
              <h2 className="text-2xl font-semibold text-slate-600 mb-2">Select a Conversation</h2>
              <p className="text-slate-500">Choose a conversation from the sidebar to start messaging</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Enhanced Background with Purple Theme */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100">
        <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-white/90 via-transparent to-transparent"></div>
        
        {/* Floating Elements */}
        <div className="absolute top-20 left-20 w-32 h-32 bg-purple-200/30 rounded-full blur-xl animate-float"></div>
        <div className="absolute top-40 right-32 w-24 h-24 bg-indigo-200/30 rounded-full blur-xl animate-float-delayed"></div>
        <div className="absolute bottom-20 left-1/3 w-40 h-40 bg-violet-200/30 rounded-full blur-xl animate-float"></div>
      </div>
      
      {/* Enhanced Navigation */}
      <div className="relative z-10">
        <nav className="flex items-center justify-between p-6 backdrop-blur-lg bg-white/70 border-b border-purple-100/50">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl shadow-lg">
              <Trophy className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                Khel Bhoomi
              </h1>
              <p className="text-xs text-purple-500 font-medium">Sports Community</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <Button variant="ghost" className="text-slate-700 hover:text-purple-600 hover:bg-purple-50" onClick={() => navigate('/about')}>
              About
            </Button>
            <Button variant="ghost" className="text-slate-700 hover:text-purple-600 hover:bg-purple-50" onClick={() => navigate('/features')}>
              Features
            </Button>
            <Button variant="ghost" className="text-slate-700 hover:text-purple-600 hover:bg-purple-50">
              Community
            </Button>
            <Button 
              variant="outline" 
              className="border-purple-200 text-purple-600 hover:bg-purple-50" 
              onClick={() => navigate('/auth')}
            >
              Login
            </Button>
            <Button 
              className="bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white shadow-lg" 
              onClick={() => navigate('/auth')}
            >
              Join Now
            </Button>
          </div>
        </nav>

        {/* Enhanced Hero Section */}
        <div className="container mx-auto px-6 pt-16 pb-24">
          <div className="max-w-6xl mx-auto">
            {/* Hero Content */}
            <div className="text-center mb-16">
              <div className="inline-flex items-center space-x-2 bg-purple-100/50 backdrop-blur-sm px-4 py-2 rounded-full mb-8">
                <Star className="h-4 w-4 text-purple-500" />
                <span className="text-purple-700 font-medium text-sm">India's Premier Sports Social Platform</span>
              </div>
              
              <h1 className="hero-title text-7xl md:text-8xl font-black text-slate-900 mb-8 leading-none">
                <span className="block">Welcome to</span>
                <span className="block bg-gradient-to-r from-purple-600 via-indigo-600 to-violet-600 bg-clip-text text-transparent">
                  Khel Bhoomi
                </span>
              </h1>
              
              <p className="text-2xl text-slate-600 mb-12 max-w-3xl mx-auto leading-relaxed font-light">
                Where athletes shine, scouts discover champions, and fans celebrate the spirit of sports. 
                Join India's most vibrant sports community today.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16">
                <Button 
                  size="lg" 
                  className="bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white px-10 py-6 text-xl rounded-2xl shadow-2xl hover:shadow-purple-500/25 transform hover:scale-105 transition-all duration-300"
                  onClick={() => navigate('/auth')}
                >
                  <Trophy className="h-6 w-6 mr-3" />
                  Explore Sports Feed
                </Button>
                
                <Button 
                  size="lg" 
                  variant="outline" 
                  className="border-2 border-purple-200 text-purple-600 hover:bg-purple-50 px-10 py-6 text-xl rounded-2xl shadow-xl hover:shadow-purple-500/10 transform hover:scale-105 transition-all duration-300"
                  onClick={() => navigate('/auth')}
                >
                  <Users className="h-6 w-6 mr-3" />
                  Join Community
                </Button>
              </div>

              {/* Stats Section */}
              <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto mb-16">
                <div className="text-center">
                  <div className="text-4xl font-bold text-purple-600 mb-2">10K+</div>
                  <div className="text-slate-600">Active Athletes</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-indigo-600 mb-2">500+</div>
                  <div className="text-slate-600">Professional Scouts</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-violet-600 mb-2">50K+</div>
                  <div className="text-slate-600">Sports Fans</div>
                </div>
              </div>
            </div>

            {/* Enhanced Role Selection Cards */}
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
              <Card className="glass-card group hover:scale-105 transition-all duration-500 border-0 shadow-2xl overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10"></div>
                <CardHeader className="text-center pb-6 relative z-10">
                  <div className="mx-auto w-20 h-20 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
                    <Trophy className="h-10 w-10 text-white" />
                  </div>
                  <CardTitle className="text-2xl font-bold text-slate-800 mb-2">Athletes</CardTitle>
                  <p className="text-blue-600 font-semibold">Showcase Your Talent</p>
                </CardHeader>
                <CardContent className="text-center relative z-10">
                  <p className="text-slate-600 mb-6 leading-relaxed">
                    Build your sports profile, share achievements, connect with scouts, and get discovered by teams looking for talent like yours.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center mb-6">
                    <Badge variant="secondary" className="bg-blue-100 text-blue-600">Portfolio</Badge>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-600">Achievements</Badge>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-600">Networking</Badge>
                  </div>
                  <Button 
                    className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white shadow-lg"
                    onClick={() => navigate('/auth')}
                  >
                    Join as Athlete
                  </Button>
                </CardContent>
              </Card>

              <Card className="glass-card group hover:scale-105 transition-all duration-500 border-0 shadow-2xl overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-r from-green-500/10 to-emerald-500/10"></div>
                <CardHeader className="text-center pb-6 relative z-10">
                  <div className="mx-auto w-20 h-20 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
                    <Target className="h-10 w-10 text-white" />
                  </div>
                  <CardTitle className="text-2xl font-bold text-slate-800 mb-2">Scouts</CardTitle>
                  <p className="text-green-600 font-semibold">Discover Champions</p>
                </CardHeader>
                <CardContent className="text-center relative z-10">
                  <p className="text-slate-600 mb-6 leading-relaxed">
                    Find the next sports stars, evaluate player performance, build winning teams, and connect with emerging talent across India.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center mb-6">
                    <Badge variant="secondary" className="bg-green-100 text-green-600">Talent Hunt</Badge>
                    <Badge variant="secondary" className="bg-green-100 text-green-600">Analytics</Badge>
                    <Badge variant="secondary" className="bg-green-100 text-green-600">Recruiting</Badge>
                  </div>
                  <Button 
                    className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white shadow-lg"
                    onClick={() => navigate('/auth')}
                  >
                    Join as Scout
                  </Button>
                </CardContent>
              </Card>

              <Card className="glass-card group hover:scale-105 transition-all duration-500 border-0 shadow-2xl overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10"></div>
                <CardHeader className="text-center pb-6 relative z-10">
                  <div className="mx-auto w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
                    <Heart className="h-10 w-10 text-white" />
                  </div>
                  <CardTitle className="text-2xl font-bold text-slate-800 mb-2">Fans</CardTitle>
                  <p className="text-purple-600 font-semibold">Celebrate Sports</p>
                </CardHeader>
                <CardContent className="text-center relative z-10">
                  <p className="text-slate-600 mb-6 leading-relaxed">
                    Follow your favorite athletes, discuss matches, celebrate victories, and be part of India's most passionate sports community.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center mb-6">
                    <Badge variant="secondary" className="bg-purple-100 text-purple-600">Follow</Badge>
                    <Badge variant="secondary" className="bg-purple-100 text-purple-600">Discuss</Badge>
                    <Badge variant="secondary" className="bg-purple-100 text-purple-600">Celebrate</Badge>
                  </div>
                  <Button 
                    className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg"
                    onClick={() => navigate('/auth')}
                  >
                    Join as Fan
                  </Button>
                </CardContent>
              </Card>
            </div>

            {/* Enhanced Sports Showcase */}
            <div className="mb-16">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-slate-800 mb-4">Sports We Love</h2>
                <p className="text-xl text-slate-600">From grassroots to professional level across India</p>
              </div>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1531415074968-036ba1b575da?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw3fHxjcmlja2V0fGVufDB8fHx8MTc1NzUzMTYxMnww&ixlib=rb-4.1.0&q=85" 
                      alt="Cricket - India's Passion" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Cricket</h3>
                      <p className="text-xs opacity-90">India's heartbeat sport</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1608245449230-4ac19066d2d0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxhdGhsZXRlfGVufDB8fHx8MTc1NzUzMTYxMnww&ixlib=rb-4.1.0&q=85" 
                      alt="Elite Basketball" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Basketball</h3>
                      <p className="text-xs opacity-90">High-performance training</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1697767394715-75e8183e85bb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxzcG9ydHMlMjBjb21tdW5pdHl8ZW58MHx8fHwxNzU3NTMxNjA1fDA&ixlib=rb-4.1.0&q=85" 
                      alt="Football Community" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Football</h3>
                      <p className="text-xs opacity-90">Global sport, local community</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1461896836934-ffe607ba8211?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdGhsZXRlfGVufDB8fHx8MTc1NzUzMTYxMnww&ixlib=rb-4.1.0&q=85" 
                      alt="Track and Field" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Track & Field</h3>
                      <p className="text-xs opacity-90">Athletic excellence</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1544551763-46a013bb70d5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHx0ZW5uaXN8ZW58MHx8fHwxNzU3NTMxNjEyfDA&ixlib=rb-4.1.0&q=85" 
                      alt="Tennis" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Tennis</h3>
                      <p className="text-xs opacity-90">Precision and power</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw2fHxzd2ltbWluZ3xlbnwwfHx8fDE3NTc1MzE2MTJ8MA&ixlib=rb-4.1.0&q=85" 
                      alt="Swimming" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Swimming</h3>
                      <p className="text-xs opacity-90">Aquatic excellence</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1578662996442-48f60103fc96?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxiYWRtaW50b258ZW58MHx8fHwxNzU3NTMxNjEyfDA&ixlib=rb-4.1.0&q=85" 
                      alt="Badminton" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Badminton</h3>
                      <p className="text-xs opacity-90">Speed and agility</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card overflow-hidden group cursor-pointer">
                  <div className="relative">
                    <img 
                      src="https://images.unsplash.com/photo-1578068121672-729c25d5d2b4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxob2NrZXl8ZW58MHx8fHwxNzU3NTMxNjEyfDA&ixlib=rb-4.1.0&q=85" 
                      alt="Hockey" 
                      className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <h3 className="text-lg font-bold mb-1">Hockey</h3>
                      <p className="text-xs opacity-90">India's national sport</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Success Stories Section */}
            <div className="mb-16">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-slate-800 mb-4">Success Stories</h2>
                <p className="text-xl text-slate-600">Athletes discovered through our platform</p>
              </div>
              
              <div className="grid md:grid-cols-3 gap-8">
                <Card className="glass-card border-0 shadow-xl">
                  <CardContent className="p-6">
                    <div className="text-center">
                      <Avatar className="w-20 h-20 mx-auto mb-4">
                        <AvatarFallback className="bg-gradient-to-r from-green-500 to-emerald-500 text-white text-xl">RK</AvatarFallback>
                      </Avatar>
                      <h3 className="text-xl font-bold text-slate-800 mb-2">Rajesh Kumar</h3>
                      <Badge className="bg-blue-100 text-blue-700 mb-4">Basketball Athlete</Badge>
                      <p className="text-slate-600 mb-4">"Khel Bhoomi connected me with professional scouts. Now I'm playing in the national league!"</p>
                      <div className="flex justify-center">
                        <Badge variant="secondary" className="bg-yellow-100 text-yellow-600">
                          <Trophy className="h-3 w-3 mr-1" />
                          National Player
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="glass-card border-0 shadow-xl">
                  <CardContent className="p-6">
                    <div className="text-center">
                      <Avatar className="w-20 h-20 mx-auto mb-4">
                        <AvatarFallback className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xl">PS</AvatarFallback>
                      </Avatar>
                      <h3 className="text-xl font-bold text-slate-800 mb-2">Priya Sharma</h3>
                      <Badge className="bg-green-100 text-green-700 mb-4">Track & Field</Badge>
                      <p className="text-slate-600 mb-4">"The exposure I got here helped me get into the Olympic training program. Dreams do come true!"</p>
                      <div className="flex justify-center">
                        <Badge variant="secondary" className="bg-yellow-100 text-yellow-600">
                          <Medal className="h-3 w-3 mr-1" />
                          Olympic Trainee
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="glass-card border-0 shadow-xl">
                  <CardContent className="p-6">
                    <div className="text-center">
                      <Avatar className="w-20 h-20 mx-auto mb-4">
                        <AvatarFallback className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-xl">AV</AvatarFallback>
                      </Avatar>
                      <h3 className="text-xl font-bold text-slate-800 mb-2">Arjun Verma</h3>
                      <Badge className="bg-purple-100 text-purple-700 mb-4">Cricket</Badge>
                      <p className="text-slate-600 mb-4">"From a small town to IPL trials - Khel Bhoomi made it possible by connecting me with the right people!"</p>
                      <div className="flex justify-center">
                        <Badge variant="secondary" className="bg-yellow-100 text-yellow-600">
                          <Star className="h-3 w-3 mr-1" />
                          IPL Prospect
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Features Preview Section */}
            <div className="mb-16">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-slate-800 mb-4">Why Choose Khel Bhoomi?</h2>
                <p className="text-xl text-slate-600">Everything you need to excel in sports</p>
              </div>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Search className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">Talent Discovery</h3>
                  <p className="text-slate-600">Connect with scouts and get discovered by professional teams</p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Users className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">Community</h3>
                  <p className="text-slate-600">Join India's largest sports community and network</p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <TrendingUp className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">Performance Tracking</h3>
                  <p className="text-slate-600">Track your progress and showcase achievements</p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <MessageCircle className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">Direct Messaging</h3>
                  <p className="text-slate-600">Connect directly with athletes, scouts, and fans</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Section */}
        <footer className="relative z-10 bg-gradient-to-r from-slate-900 to-slate-800 text-white">
          <div className="container mx-auto px-6 py-16">
            <div className="grid md:grid-cols-4 gap-8">
              {/* Brand Column */}
              <div className="col-span-1">
                <div className="flex items-center space-x-3 mb-6">
                  <div className="p-2 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl shadow-lg">
                    <Trophy className="h-8 w-8 text-white" />
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">
                      Khel Bhoomi
                    </h1>
                    <p className="text-sm text-purple-300 font-medium">Sports Community</p>
                  </div>
                </div>
                <p className="text-slate-300 mb-6 leading-relaxed">
                  India's premier sports social platform connecting athletes, scouts, and fans. 
                  Discover talent, celebrate achievements, and be part of the sports revolution.
                </p>
                <div className="flex space-x-4">
                  <Button size="sm" variant="ghost" className="text-slate-300 hover:text-white hover:bg-slate-700">
                    <Users className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="ghost" className="text-slate-300 hover:text-white hover:bg-slate-700">
                    <MessageCircle className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="ghost" className="text-slate-300 hover:text-white hover:bg-slate-700">
                    <Share2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Quick Links */}
              <div>
                <h3 className="text-lg font-semibold mb-6 text-white">Quick Links</h3>
                <div className="space-y-3">
                  <div>
                    <button 
                      className="text-slate-300 hover:text-purple-400 transition-colors text-left"
                      onClick={() => navigate('/auth')}
                    >
                      Join Community
                    </button>
                  </div>
                  <div>
                    <button 
                      className="text-slate-300 hover:text-purple-400 transition-colors text-left"
                      onClick={() => navigate('/features')}
                    >
                      Features
                    </button>
                  </div>
                  <div>
                    <button 
                      className="text-slate-300 hover:text-purple-400 transition-colors text-left"
                      onClick={() => navigate('/about')}
                    >
                      About Us
                    </button>
                  </div>
                  <div>
                    <button 
                      className="text-slate-300 hover:text-purple-400 transition-colors text-left"
                      onClick={() => navigate('/auth')}
                    >
                      For Athletes
                    </button>
                  </div>
                  <div>
                    <button 
                      className="text-slate-300 hover:text-purple-400 transition-colors text-left"
                      onClick={() => navigate('/auth')}
                    >
                      For Scouts
                    </button>
                  </div>
                </div>
              </div>

              {/* Sports Categories */}
              <div>
                <h3 className="text-lg font-semibold mb-6 text-white">Sports Categories</h3>
                <div className="space-y-3">
                  <div className="text-slate-300">Cricket</div>
                  <div className="text-slate-300">Basketball</div>
                  <div className="text-slate-300">Football</div>
                  <div className="text-slate-300">Track & Field</div>
                  <div className="text-slate-300">Tennis</div>
                  <div className="text-slate-300">Badminton</div>
                  <div className="text-slate-300">Hockey</div>
                  <div className="text-slate-300">Swimming</div>
                </div>
              </div>

              {/* Support & Info */}
              <div>
                <h3 className="text-lg font-semibold mb-6 text-white">Support & Info</h3>
                <div className="space-y-3">
                  <div className="text-slate-300">Help Center</div>
                  <div className="text-slate-300">Privacy Policy</div>
                  <div className="text-slate-300">Terms of Service</div>
                  <div className="text-slate-300">Community Guidelines</div>
                  <div className="text-slate-300">Contact Support</div>
                  <div className="text-slate-300">Safety Center</div>
                </div>
              </div>
            </div>

            {/* Bottom Footer */}
            <div className="border-t border-slate-700 pt-8 mt-12">
              <div className="flex flex-col md:flex-row justify-between items-center">
                <div className="text-slate-400 text-sm mb-4 md:mb-0">
                  © 2025 Khel Bhoomi. All rights reserved. Empowering Indian sports since 2025.
                </div>
                <div className="flex items-center space-x-6 text-sm text-slate-400">
                  <span>Made with ❤️ for Indian Sports</span>
                  <Badge className="bg-green-100 text-green-700">
                    <span className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      <span>Live</span>
                    </span>
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </footer>
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
  const navigate = useNavigate();

  const fillDemoCredentials = (username, password) => {
    setFormData({
      ...formData,
      username: username,
      password: password
    });
    toast({
      title: "Demo credentials filled!",
      description: `Ready to login as ${username}`,
    });
  };

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
      
      // Navigate to dashboard after successful login/registration
      navigate('/dashboard');
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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100 p-4">
      <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
      
      <Card className="w-full max-w-md glass-card border-0 shadow-2xl relative z-10">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl shadow-lg">
              <Trophy className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                Khel Bhoomi
              </h1>
              <p className="text-xs text-purple-500 font-medium">Sports Community</p>
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-slate-800">
            {isLogin ? 'Welcome Back' : 'Join the Community'}
          </CardTitle>
          <CardDescription className="text-slate-600">
            {isLogin ? 'Sign in to your account' : 'Create your sports profile'}
          </CardDescription>
        </CardHeader>

        <CardContent>
          {/* Demo Login Credentials Section */}
          <div className="mb-6 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-100">
            <h3 className="text-sm font-semibold text-purple-700 mb-3 flex items-center">
              <Trophy className="h-4 w-4 mr-2" />
              Quick Demo Access
            </h3>
            <div className="grid grid-cols-1 gap-2 text-xs">
              <div className="flex justify-between items-center p-2 bg-white/60 rounded-lg hover:bg-white/80 transition-colors cursor-pointer" 
                   onClick={() => fillDemoCredentials('demo_athlete', 'demo123')}>
                <span className="font-medium text-slate-600">👤 Athlete:</span>
                <div className="text-right">
                  <div className="text-purple-600 font-mono hover:text-purple-700">demo_athlete</div>
                  <div className="text-slate-500">demo123</div>
                </div>
              </div>
              <div className="flex justify-between items-center p-2 bg-white/60 rounded-lg hover:bg-white/80 transition-colors cursor-pointer"
                   onClick={() => fillDemoCredentials('demo_scout', 'demo123')}>
                <span className="font-medium text-slate-600">🎯 Scout:</span>
                <div className="text-right">
                  <div className="text-purple-600 font-mono hover:text-purple-700">demo_scout</div>
                  <div className="text-slate-500">demo123</div>
                </div>
              </div>
              <div className="flex justify-between items-center p-2 bg-white/60 rounded-lg hover:bg-white/80 transition-colors cursor-pointer"
                   onClick={() => fillDemoCredentials('demo_fan', 'demo123')}>
                <span className="font-medium text-slate-600">❤️ Fan:</span>
                <div className="text-right">
                  <div className="text-purple-600 font-mono hover:text-purple-700">demo_fan</div>
                  <div className="text-slate-500">demo123</div>
                </div>
              </div>
            </div>
            <p className="text-xs text-purple-600 mt-2 text-center">
              Click any account to auto-fill login credentials
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="username" className="text-slate-700">Username</Label>
              <Input
                id="username"
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                required
                className="mt-1 focus:ring-purple-500 focus:border-purple-500"
                placeholder="Enter username or use demo accounts above"
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
                    className="mt-1 focus:ring-purple-500 focus:border-purple-500"
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
                    className="mt-1 focus:ring-purple-500 focus:border-purple-500"
                  />
                </div>

                <div>
                  <Label htmlFor="role" className="text-slate-700">I am a...</Label>
                  <Select value={formData.role} onValueChange={(value) => setFormData({...formData, role: value})}>
                    <SelectTrigger className="mt-1 focus:ring-purple-500 focus:border-purple-500">
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
                className="mt-1 focus:ring-purple-500 focus:border-purple-500"
              />
            </div>

            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white"
              disabled={loading}
            >
              {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
            </Button>

            <p className="text-center text-sm text-slate-600">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                className="text-purple-500 hover:text-purple-600 font-medium"
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

// Enhanced Feed Component
const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ content: '', post_type: 'text', sports_tags: [] });
  const [loading, setLoading] = useState(false);
  const [comments, setComments] = useState({});
  const [newComment, setNewComment] = useState({});
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

  const toggleComments = (postId) => {
    setComments(prev => ({
      ...prev,
      [postId]: !prev[postId]
    }));
  };

  const addComment = (postId) => {
    if (!newComment[postId]?.trim()) return;
    
    // Mock comment addition
    toast({
      title: "Comment added!",
      description: "Your comment has been posted."
    });
    
    setNewComment(prev => ({
      ...prev,
      [postId]: ''
    }));
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'athlete': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'scout': return 'bg-green-100 text-green-700 border-green-200';
      case 'fan': return 'bg-purple-100 text-purple-700 border-purple-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'athlete': return <Medal className="h-3 w-3" />;
      case 'scout': return <Target className="h-3 w-3" />;
      case 'fan': return <Heart className="h-3 w-3" />;
      default: return null;
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-6">
      {/* Enhanced Create Post Card */}
      <Card className="glass-card border-0 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-start space-x-4">
            <Avatar className="w-12 h-12">
              <AvatarFallback className="bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-semibold">
                {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            
            <div className="flex-1 space-y-4">
              <Textarea
                placeholder={`What's happening in sports, ${user?.full_name?.split(' ')[0] || user?.username}?`}
                value={newPost.content}
                onChange={(e) => setNewPost({...newPost, content: e.target.value})}
                className="border-0 resize-none focus:ring-0 text-lg placeholder:text-slate-400 min-h-[100px]"
                rows={4}
              />
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Button variant="ghost" size="sm" className="text-slate-500 hover:text-purple-600 hover:bg-purple-50">
                    <Camera className="h-4 w-4 mr-1" />
                    Photo
                  </Button>
                  <Button variant="ghost" size="sm" className="text-slate-500 hover:text-purple-600 hover:bg-purple-50">
                    <Video className="h-4 w-4 mr-1" />
                    Video
                  </Button>
                  <Button variant="ghost" size="sm" className="text-slate-500 hover:text-purple-600 hover:bg-purple-50">
                    <Award className="h-4 w-4 mr-1" />
                    Achievement
                  </Button>
                </div>
                
                <Button 
                  onClick={createPost}
                  disabled={loading || !newPost.content.trim()}
                  className="bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white rounded-xl px-8"
                >
                  {loading ? 'Posting...' : 'Post'}
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Enhanced Posts Feed */}
      <div className="space-y-6">
        {posts.map((post) => (
          <Card key={post.id} className="glass-card border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-0">
              {/* Post Header */}
              <div className="p-6 pb-4">
                <div className="flex items-start space-x-4">
                  <Avatar className="w-12 h-12">
                    <AvatarFallback className="bg-slate-100 text-slate-600 font-semibold">
                      {post.username?.charAt(0)}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h4 className="font-semibold text-slate-800 text-lg">{post.username}</h4>
                      <Badge className={`text-xs px-2 py-1 border ${getRoleColor(post.user_role)}`}>
                        <span className="flex items-center space-x-1">
                          {getRoleIcon(post.user_role)}
                          <span className="capitalize">{post.user_role}</span>
                        </span>
                      </Badge>
                    </div>
                    <p className="text-sm text-slate-500">
                      {new Date(post.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                  
                  <Button variant="ghost" size="sm" className="text-slate-400 hover:text-slate-600">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Post Content */}
              <div className="px-6 pb-4">
                <p className="text-slate-700 text-lg leading-relaxed mb-4">{post.content}</p>
                
                {post.image_url && (
                  <div className="mb-4 rounded-xl overflow-hidden">
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
                      <Badge key={index} variant="secondary" className="text-xs bg-purple-100 text-purple-600 hover:bg-purple-200 cursor-pointer">
                        #{tag}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>

              {/* Post Actions */}
              <div className="border-t border-slate-100 p-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-6">
                    <Button variant="ghost" size="sm" className="hover:text-red-500 hover:bg-red-50 transition-colors">
                      <Heart className="h-5 w-5 mr-2" />
                      <span className="font-medium">{post.likes}</span>
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="hover:text-blue-500 hover:bg-blue-50 transition-colors"
                      onClick={() => toggleComments(post.id)}
                    >
                      <MessageCircle className="h-5 w-5 mr-2" />
                      <span className="font-medium">{post.comments}</span>
                    </Button>
                    <Button variant="ghost" size="sm" className="hover:text-green-500 hover:bg-green-50 transition-colors">
                      <Share2 className="h-5 w-5 mr-2" />
                      Share
                    </Button>
                  </div>
                </div>

                {/* Comments Section */}
                {comments[post.id] && (
                  <div className="space-y-4 border-t border-slate-100 pt-4">
                    {/* Add Comment */}
                    <div className="flex items-center space-x-3">
                      <Avatar className="w-8 h-8">
                        <AvatarFallback className="bg-purple-100 text-purple-600 text-sm">
                          {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 flex items-center space-x-2">
                        <Input
                          placeholder="Write a comment..."
                          value={newComment[post.id] || ''}
                          onChange={(e) => setNewComment(prev => ({
                            ...prev,
                            [post.id]: e.target.value
                          }))}
                          className="border-slate-200 focus:border-purple-300 focus:ring-purple-300"
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                              addComment(post.id);
                            }
                          }}
                        />
                        <Button 
                          size="sm" 
                          onClick={() => addComment(post.id)}
                          className="bg-purple-500 hover:bg-purple-600 text-white"
                        >
                          <Send className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>

                    {/* Sample Comments */}
                    <div className="space-y-3">
                      <div className="flex items-start space-x-3">
                        <Avatar className="w-8 h-8">
                          <AvatarFallback className="bg-blue-100 text-blue-600 text-sm">S</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <div className="bg-slate-50 rounded-lg p-3">
                            <div className="flex items-center space-x-2 mb-1">
                              <span className="font-semibold text-sm">sports_fan_123</span>
                              <Badge className="text-xs bg-purple-100 text-purple-600 border-purple-200">Fan</Badge>
                            </div>
                            <p className="text-sm text-slate-700">Great performance! Keep it up! 🔥</p>
                          </div>
                          <div className="flex items-center space-x-4 mt-2 text-xs text-slate-500">
                            <button className="hover:text-purple-600">Like</button>
                            <button className="hover:text-purple-600">Reply</button>
                            <span>2h</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

// Profile Dashboard Component
const ProfileDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const AthleteProfile = () => (
    <div className="space-y-6">
      {/* Profile Header */}
      <Card className="glass-card border-0 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-start space-x-6">
            <Avatar className="w-24 h-24">
              <AvatarFallback className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-2xl font-bold">
                {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h1 className="text-3xl font-bold text-slate-800">{user?.full_name || user?.username}</h1>
                <Badge className="bg-blue-100 text-blue-700 border-blue-200">
                  <Medal className="h-3 w-3 mr-1" />
                  Athlete
                </Badge>
              </div>
              <p className="text-slate-600 mb-4">{user?.bio || "Passionate athlete dedicated to excellence in sports"}</p>
              <div className="flex items-center space-x-4 text-sm text-slate-500">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span>Mumbai, India</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>Joined {new Date(user?.created_at).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })}</span>
                </div>
              </div>
            </div>
            <Button className="bg-purple-500 hover:bg-purple-600 text-white">
              <Edit className="h-4 w-4 mr-2" />
              Edit Profile
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Stats Cards */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-blue-600 mb-1">156</div>
            <div className="text-sm text-slate-600">Posts</div>
          </CardContent>
        </Card>
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-green-600 mb-1">2.3K</div>
            <div className="text-sm text-slate-600">Followers</div>
          </CardContent>
        </Card>
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-purple-600 mb-1">45</div>
            <div className="text-sm text-slate-600">Achievements</div>
          </CardContent>
        </Card>
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-indigo-600 mb-1">8.5</div>
            <div className="text-sm text-slate-600">Rating</div>
          </CardContent>
        </Card>
      </div>

      {/* Achievements & Skills */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="glass-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Award className="h-5 w-5 text-yellow-500" />
              <span>Recent Achievements</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center space-x-3 p-3 bg-yellow-50 rounded-lg">
              <Trophy className="h-8 w-8 text-yellow-500" />
              <div>
                <div className="font-semibold">State Championship Winner</div>
                <div className="text-sm text-slate-600">Basketball - 2024</div>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
              <Medal className="h-8 w-8 text-blue-500" />
              <div>
                <div className="font-semibold">Best Player Award</div>
                <div className="text-sm text-slate-600">Regional Tournament - 2024</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <span>Skills & Stats</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Shooting Accuracy</span>
                <span className="text-sm text-slate-600">85%</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{width: '85%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Speed & Agility</span>
                <span className="text-sm text-slate-600">92%</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{width: '92%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Team Work</span>
                <span className="text-sm text-slate-600">95%</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{width: '95%'}}></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );

  const ScoutProfile = () => (
    <div className="space-y-6">
      {/* Profile Header */}
      <Card className="glass-card border-0 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-start space-x-6">
            <Avatar className="w-24 h-24">
              <AvatarFallback className="bg-gradient-to-r from-green-500 to-emerald-500 text-white text-2xl font-bold">
                {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h1 className="text-3xl font-bold text-slate-800">{user?.full_name || user?.username}</h1>
                <Badge className="bg-green-100 text-green-700 border-green-200">
                  <Target className="h-3 w-3 mr-1" />
                  Scout
                </Badge>
              </div>
              <p className="text-slate-600 mb-4">{user?.bio || "Professional scout discovering the next generation of sports talent"}</p>
              <div className="flex items-center space-x-4 text-sm text-slate-500">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span>Delhi, India</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>Joined {new Date(user?.created_at).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })}</span>
                </div>
              </div>
            </div>
            <Button className="bg-purple-500 hover:bg-purple-600 text-white">
              <Edit className="h-4 w-4 mr-2" />
              Edit Profile
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Scout Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-green-600 mb-1">89</div>
            <div className="text-sm text-slate-600">Athletes Scouted</div>
          </CardContent>
        </Card>
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-blue-600 mb-1">23</div>
            <div className="text-sm text-slate-600">Successful Placements</div>
          </CardContent>
        </Card>
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-purple-600 mb-1">15</div>
            <div className="text-sm text-slate-600">Teams Connected</div>
          </CardContent>
        </Card>
        <Card className="glass-card border-0 shadow-lg">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-indigo-600 mb-1">95%</div>
            <div className="text-sm text-slate-600">Success Rate</div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Discoveries & Expertise */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="glass-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <UserCheck className="h-5 w-5 text-green-500" />
              <span>Recent Discoveries</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
              <Avatar className="w-10 h-10">
                <AvatarFallback className="bg-blue-500 text-white">RK</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="font-semibold">Rajesh Kumar</div>
                <div className="text-sm text-slate-600">Basketball • 19 years • Mumbai</div>
              </div>
              <Badge variant="secondary" className="bg-green-100 text-green-600">Recruited</Badge>
            </div>
            <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
              <Avatar className="w-10 h-10">
                <AvatarFallback className="bg-purple-500 text-white">PS</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="font-semibold">Priya Sharma</div>
                <div className="text-sm text-slate-600">Track & Field • 21 years • Delhi</div>
              </div>
              <Badge variant="secondary" className="bg-yellow-100 text-yellow-600">In Review</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BookOpen className="h-5 w-5 text-purple-500" />
              <span>Expertise & Focus</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <Badge className="bg-blue-100 text-blue-600">Basketball</Badge>
              <Badge className="bg-green-100 text-green-600">Track & Field</Badge>
              <Badge className="bg-purple-100 text-purple-600">Swimming</Badge>
              <Badge className="bg-indigo-100 text-indigo-600">Football</Badge>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Age Group</span>
                <span className="text-sm text-slate-600">16-25 years</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Experience</span>
                <span className="text-sm text-slate-600">8+ years</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Specialization</span>
                <span className="text-sm text-slate-600">Youth Development</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-4">
      {user?.role === 'athlete' ? <AthleteProfile /> : user?.role === 'scout' ? <ScoutProfile /> : <AthleteProfile />}
    </div>
  );
};

// Main Dashboard Component
const Dashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('feed');
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100">
      <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
      
      {/* Enhanced Top Navigation */}
      <nav className="relative z-10 bg-white/80 backdrop-blur-xl border-b border-purple-100/50 shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
                <div className="p-2 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl shadow-lg">
                  <Trophy className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                    Khel Bhoomi
                  </h1>
                  <p className="text-xs text-purple-500 font-medium">Sports Community</p>
                </div>
              </div>
              
              <div className="hidden md:flex items-center space-x-2">
                <Button 
                  variant={activeTab === 'feed' ? 'default' : 'ghost'} 
                  onClick={() => setActiveTab('feed')}
                  className={activeTab === 'feed' 
                    ? 'bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white' 
                    : 'text-slate-600 hover:text-purple-600 hover:bg-purple-50'
                  }
                >
                  <Home className="h-4 w-4 mr-2" />
                  Feed
                </Button>
                <Button 
                  variant={activeTab === 'profile' ? 'default' : 'ghost'} 
                  onClick={() => setActiveTab('profile')}
                  className={activeTab === 'profile' 
                    ? 'bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white' 
                    : 'text-slate-600 hover:text-purple-600 hover:bg-purple-50'
                  }
                >
                  <User className="h-4 w-4 mr-2" />
                  Profile
                </Button>
                <Button 
                  variant="ghost" 
                  className="text-slate-600 hover:text-purple-600 hover:bg-purple-50"
                >
                  <Search className="h-4 w-4 mr-2" />
                  Explore
                </Button>
                <Button 
                  variant="ghost" 
                  className="text-slate-600 hover:text-purple-600 hover:bg-purple-50"
                  onClick={() => navigate('/messages')}
                >
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Messages
                </Button>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" className="text-slate-600 hover:text-purple-600 hover:bg-purple-50">
                <Search className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="sm" className="text-slate-600 hover:text-purple-600 hover:bg-purple-50">
                <Bell className="h-5 w-5" />
              </Button>
              
              <div className="flex items-center space-x-3">
                <Avatar className="h-10 w-10">
                  <AvatarFallback className="bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-semibold">
                    {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
                  </AvatarFallback>
                </Avatar>
                <div className="hidden md:block">
                  <div className="text-sm font-medium text-slate-700">
                    {user?.full_name || user?.username}
                  </div>
                  <div className="text-xs text-purple-500 capitalize">
                    {user?.role}
                  </div>
                </div>
              </div>
              
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={logout}
                className="text-slate-600 hover:text-red-500 hover:bg-red-50"
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
        {activeTab === 'profile' && <ProfileDashboard />}
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
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-100">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Trophy className="h-8 w-8 text-white animate-pulse" />
          </div>
          <p className="text-slate-600 font-medium">Loading Khel Bhoomi...</p>
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
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/messages" 
              element={
                <ProtectedRoute>
                  <MessagesPage />
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
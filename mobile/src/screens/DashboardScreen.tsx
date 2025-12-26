/**
 * Dashboard Screen
 * Main overview with reputation scores, alerts, and trends
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useQuery } from '@tanstack/react-query';
import { fetchDashboardData } from '../api/client';

const screenWidth = Dimensions.get('window').width;

export default function DashboardScreen({ navigation }) {
  const { data, isLoading, refetch, isRefetching } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboardData,
  });

  const chartConfig = {
    backgroundGradientFrom: '#fff',
    backgroundGradientTo: '#fff',
    color: (opacity = 1) => `rgba(99, 102, 241, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.5,
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Dashboard</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Settings')}>
          <Icon name="cog-outline" size={24} color="#333" />
        </TouchableOpacity>
      </View>

      {/* Stats Cards */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Icon name="domain" size={32} color="#6366f1" />
          <Text style={styles.statValue}>{data?.totalEntities || 0}</Text>
          <Text style={styles.statLabel}>Entities</Text>
        </View>

        <View style={styles.statCard}>
          <Icon name="message-text" size={32} color="#10b981" />
          <Text style={styles.statValue}>{data?.totalMentions || 0}</Text>
          <Text style={styles.statLabel}>Mentions</Text>
        </View>

        <View style={styles.statCard}>
          <Icon name="bell" size={32} color="#f59e0b" />
          <Text style={styles.statValue}>{data?.unreadAlerts || 0}</Text>
          <Text style={styles.statLabel}>Alerts</Text>
        </View>

        <View style={styles.statCard}>
          <Icon name="trending-up" size={32} color="#8b5cf6" />
          <Text style={styles.statValue}>{data?.avgReputation || 0}</Text>
          <Text style={styles.statLabel}>Avg Score</Text>
        </View>
      </View>

      {/* Reputation Trend Chart */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Reputation Trend (7 Days)</Text>
        <LineChart
          data={{
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
              {
                data: data?.reputationTrend || [70, 72, 71, 75, 73, 76, 78],
              },
            ],
          }}
          width={screenWidth - 40}
          height={220}
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />
      </View>

      {/* Recent Alerts */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Recent Alerts</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Alerts')}>
            <Text style={styles.viewAllText}>View All</Text>
          </TouchableOpacity>
        </View>

        {data?.recentAlerts?.slice(0, 3).map((alert) => (
          <View key={alert.id} style={styles.alertCard}>
            <Icon
              name={
                alert.severity === 'critical'
                  ? 'alert-circle'
                  : alert.severity === 'high'
                  ? 'alert'
                  : 'information'
              }
              size={24}
              color={
                alert.severity === 'critical'
                  ? '#ef4444'
                  : alert.severity === 'high'
                  ? '#f59e0b'
                  : '#3b82f6'
              }
            />
            <View style={styles.alertContent}>
              <Text style={styles.alertTitle}>{alert.title}</Text>
              <Text style={styles.alertTime}>{alert.timeAgo}</Text>
            </View>
          </View>
        ))}
      </View>

      {/* Top Entities */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Top Performing Entities</Text>

        {data?.topEntities?.slice(0, 5).map((entity) => (
          <TouchableOpacity
            key={entity.id}
            style={styles.entityCard}
            onPress={() =>
              navigation.navigate('EntityDetail', { entityId: entity.id })
            }
          >
            <View style={styles.entityInfo}>
              <Text style={styles.entityName}>{entity.name}</Text>
              <Text style={styles.entityType}>{entity.type}</Text>
            </View>
            <View style={styles.entityScore}>
              <Text
                style={[
                  styles.scoreText,
                  {
                    color:
                      entity.score >= 80
                        ? '#10b981'
                        : entity.score >= 60
                        ? '#f59e0b'
                        : '#ef4444',
                  },
                ]}
              >
                {entity.score}
              </Text>
              <Icon
                name={
                  entity.trend === 'up'
                    ? 'trending-up'
                    : entity.trend === 'down'
                    ? 'trending-down'
                    : 'trending-neutral'
                }
                size={20}
                color={
                  entity.trend === 'up'
                    ? '#10b981'
                    : entity.trend === 'down'
                    ? '#ef4444'
                    : '#64748b'
                }
              />
            </View>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#fff',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1e293b',
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 10,
  },
  statCard: {
    width: '47%',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    margin: '1.5%',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1e293b',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 14,
    color: '#64748b',
    marginTop: 4,
  },
  section: {
    backgroundColor: '#fff',
    margin: 10,
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 15,
  },
  viewAllText: {
    fontSize: 14,
    color: '#6366f1',
    fontWeight: '500',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 8,
  },
  alertCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#f8fafc',
    borderRadius: 8,
    marginBottom: 8,
  },
  alertContent: {
    flex: 1,
    marginLeft: 12,
  },
  alertTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: '#1e293b',
  },
  alertTime: {
    fontSize: 12,
    color: '#64748b',
    marginTop: 2,
  },
  entityCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#f8fafc',
    borderRadius: 8,
    marginBottom: 8,
  },
  entityInfo: {
    flex: 1,
  },
  entityName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1e293b',
  },
  entityType: {
    fontSize: 12,
    color: '#64748b',
    marginTop: 2,
    textTransform: 'capitalize',
  },
  entityScore: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  scoreText: {
    fontSize: 20,
    fontWeight: 'bold',
    marginRight: 8,
  },
});
